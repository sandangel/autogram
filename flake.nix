{
  description = "Description for the project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    devenv.url = "github:cachix/devenv";
    nix2container.url = "github:nlewo/nix2container";
    nix2container.inputs.nixpkgs.follows = "nixpkgs";
    mk-shell-bin.url = "github:rrbutani/nix-mk-shell-bin";
    fenix = {
      url = "github:nix-community/fenix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ flake-parts, fenix, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.devenv.flakeModule
      ];
      systems = [ "aarch64-darwin" ];

      perSystem = { config, self', inputs', system, lib, ... }:
        let
          pkgs = import inputs.nixpkgs {
            inherit system;
            overlays = [ fenix.overlays.default ];
          };
        in
        {
          devShells.default = with pkgs; mkShell {
            buildInputs = [
              fenix.packages.${system}.stable.toolchain
              rust-analyzer-nightly
              bun
              python3
              typescript
              cocoapods
              libiconv
              (hatch.overrideAttrs (_: rec {
                version = "1.9.3";
                src = fetchPypi {
                  pname = "hatch";
                  inherit version;
                  hash = "sha256-ZyAX40nFSPipV6X+6aovjPwsiplDBzeORahCeXK9+Nk=";
                };
                # pytest is failing because of sandbox environment
                pytestCheckPhase = "echo true";
              }))
              (rye.overrideAttrs (o: rec {
                version = "0.29.0";
                src = fetchFromGitHub {
                  owner = "astral-sh";
                  repo = "rye";
                  rev = "refs/tags/${version}";
                  hash = "sha256-rNXzhJazOi815dhqviqtfSTM60Y/5ncKBVn2YhqcKJM=";
                };
                # https://github.com/NixOS/nixpkgs/blob/master/doc/languages-frameworks/rust.section.md#vendoring-of-dependencies-vendoring-of-dependencies
                cargoDeps = rustPlatform.importCargoLock {
                  lockFile = "${src}/Cargo.lock";
                  outputHashes = {
                    "dialoguer-0.10.4" = "sha256-WDqUKOu7Y0HElpPxf2T8EpzAY3mY8sSn9lf0V0jyAFc=";
                    "monotrail-utils-0.0.1" = "sha256-ydNdg6VI+Z5wXe2bEzRtavw0rsrcJkdsJ5DvXhbaDE4=";
                  };
                };
                doCheck = false;
              }))
            ] ++ (with darwin.apple_sdk.frameworks; [
              AppKit
              WebKit
            ]);
          };
        };
    };
}

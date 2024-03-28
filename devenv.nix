{ pkgs, ... }:

{
  dotenv.disableHint = true;

  packages =
    (with pkgs; [
      gcc
      libiconv
    ])
    ++ (with pkgs.darwin.apple_sdk.frameworks; [ SystemConfiguration ]);

  languages.rust.enable = true;
  languages.rust.channel = "stable";
}

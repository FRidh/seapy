let
  nixpkgs = fetchGit {
    url = https://github.com/NixOS/nixpkgs.git;
    ref = "nixpkgs-unstable";
    rev = "cc1ae9f21b9e0ce998e706a3de1bad0b5259f22d";
  };
  pkgs = import nixpkgs {};

  python = pkgs.python3;

  pkg = python.pkgs.callPackage ./default.nix { };

  devInputs = [ python.pkgs.notebook ];
  env = python.withPackages(_: pkg.allInputs ++ devInputs);

in {
  inherit pkg env;
}
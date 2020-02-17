let
  nixpkgs = fetchGit {
    url = https://github.com/NixOS/nixpkgs.git;
    ref = "nixpkgs-unstable";
    rev = "cc1ae9f21b9e0ce998e706a3de1bad0b5259f22d"; 
  };
  pkgs = import nixpkgs {};

  pkg = pkgs.python3.pkgs.callPackage ./default.nix { };

  devInputs = [ pkgs.python3.pkgs.notebook ];
  env = pkgs.python3.withPackages(_: pkg.allInputs ++ devInputs);

in { 
  inherit pkg env;
}
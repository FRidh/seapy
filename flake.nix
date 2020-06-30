{
  description = "Statistical Energy Analysis module for Python.";

  inputs.nixpkgs.url = "nixpkgs/nixpkgs-unstable";
  inputs.utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, utils }: {
    overlay = final: prev: {
      pythonPackagesOverrides = (prev.pythonPackagesOverrides or []) ++ [
        (self: super: {
          seapy = self.callPackage ./. {};
        })
      ];
      # Remove when https://github.com/NixOS/nixpkgs/pull/91850 is fixed.
      python3 = let
        composeOverlays = nixpkgs.lib.foldl' nixpkgs.lib.composeExtensions (self: super: {});
        self = prev.python3.override {
          inherit self;
          packageOverrides = composeOverlays final.pythonPackagesOverrides;
        };
      in self;
    };
  } // (utils.lib.eachSystem [ "x86_64-linux" ] (system: {
    # Our own overlay does not get applied to nixpkgs because that would lead to
    # an infinite recursion. Therefore, we need to import nixpkgs and apply it ourselves.
    defaultPackage = (import nixpkgs {
      inherit system;
      overlays = [ self.overlay ];
    }).python3.pkgs.seapy;
  }));
}
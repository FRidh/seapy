{ buildPythonPackage
, numpy
, matplotlib
, pandas
, toolz
, networkx
, pyyaml
, pytestCheckHook
, acoustics
}:

let

  acoustics_ = acoustics.overridePythonAttrs(oldAttrs: {
    doCheck = false;
  });

in buildPythonPackage rec {
  pname = "seapy";
  version = "dev";

  src = fetchGit ./.;

  propagatedBuildInputs = [ 
    numpy
    matplotlib
    pandas
    toolz
    networkx
    pyyaml
  ];

  checkInputs = [
    pytestCheckHook
    acoustics_
  ];

  passthru.allInputs = propagatedBuildInputs ++ checkInputs;

  dontUseSetuptoolsCheck = true;
}
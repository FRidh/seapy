{ buildPythonPackage
, numpy
, matplotlib
, pandas
, toolz
, networkx
, pyyaml
, pytestCheckHook
, acoustics
, black
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
    black
  ];

  passthru.allInputs = propagatedBuildInputs ++ checkInputs;

  dontUseSetuptoolsCheck = true;

  preCheck = ''
    black --check seapy tests setup.py docs/conf.py
  '';
}
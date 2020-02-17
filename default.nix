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
, pylint
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
    pylint
  ];

  passthru.allInputs = propagatedBuildInputs ++ checkInputs;

  dontUseSetuptoolsCheck = true;

  preCheck = ''
    echo "Checking formatting with black..."
    black --check seapy tests setup.py docs/conf.py
    echo "Static analysis with pylint..."
    pylint -E seapy
  '';
}
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
, sphinx
, flit-core
}:

let

  acoustics_ = acoustics.overridePythonAttrs(oldAttrs: {
    doCheck = false;
  });

in buildPythonPackage rec {
  pname = "seapy";
  version = "0.0.0";
  format = "pyproject";

  src = ./.;

  nativeBuildInputs = [ sphinx flit-core ];

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

  postBuild = ''
    make -C docs html
    mkdir -p $doc
    mv -T docs/_build/html $doc
  '';

  outputs = [ "out" "doc" ];

  passthru.allInputs = propagatedBuildInputs ++ checkInputs;

  dontUseSetuptoolsCheck = true;

  preCheck = ''
    echo "Checking formatting with black..."
    black --check seapy tests docs/conf.py
    echo "Static analysis with pylint..."
    pylint -E seapy
  '';
}
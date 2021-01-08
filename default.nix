{pkgs ? import <nixpkgs> {}}:

pkgs.stdenv.mkDerivation {
  name = "clippy-server";
  buildInputs = [
    (pkgs.python3.withPackages (ps: with ps; [
      websockets
    ]))
  ];
}

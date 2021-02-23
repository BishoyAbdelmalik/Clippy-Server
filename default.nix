{pkgs ? import <nixpkgs> {}}:

pkgs.stdenv.mkDerivation {
  name = "clippy-server";
  buildInputs = [
    (pkgs.python3Full.withPackages (p: [p.tkinter] ))
  ];
}

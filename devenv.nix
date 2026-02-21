{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  packages = [
    pkgs.git
    pkgs.pkg-config
    pkgs.cairo
    pkgs.gobject-introspection
    pkgs.gtk3
    pkgs.enchant_2
  ];

  env.LD_LIBRARY_PATH = lib.makeLibraryPath [
    pkgs.cairo
    pkgs.gobject-introspection
    pkgs.gtk3
    pkgs.glib
    pkgs.enchant_2
  ];

  languages.python = {
    enable = true;
    poetry.enable = true;
  };
}

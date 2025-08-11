{
  description = "A TUI application for scheduling quick notifications";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pythonEnv = pkgs.python311.withPackages (
        p: with p; [
          textual
        ]
      );
    in
    {
      packages.${system}.default = pkgs.stdenv.mkDerivation {
        pname = "tui-notifier";
        version = "0.1.0";
        src = ./.;

        buildInputs = with pkgs; [
          pythonEnv
          libnotify
        ];

        installPhase = ''
                    mkdir -p $out/bin
                    cp $src/main.py $out/bin/tui-notifier-main.py
                    chmod +x $out/bin/tui-notifier-main.py

                    cat <<EOF > $out/bin/tui-notifier
          #!${pkgs.stdenv.shell}
          ${pythonEnv}/bin/python $out/bin/tui-notifier-main.py
          EOF
                    chmod +x $out/bin/tui-notifier
        '';
      };

      apps.${system}.default = {
        type = "app";
        program = "${self.packages.${system}.default}/bin/tui-notifier";
      };

      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          python311
          python311Packages.textual
          libnotify
        ];
      };
    };
}

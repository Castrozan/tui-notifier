{ pkgs, ... }:

{
  cachix.enable = false;

  packages = with pkgs; [
    git

    (python311.withPackages (
      ps: with ps; [
        textual
        black
        flake8
        mypy
        pytest
        pip
        setuptools
        wheel
      ]
    ))

    libnotify
  ];

  scripts.run.exec = "python main.py";
  scripts.format.exec = "black main.py";
  scripts.lint.exec = "flake8 main.py";
  scripts.typecheck.exec = "mypy main.py";
  scripts.test.exec = "pytest";

  enterShell = ''
    echo ""
    echo "🔔 TUI Notifier Development Environment"
    echo "======================================="
    echo ""
    echo "Available commands:"
    echo "  run        - Run the TUI notifier application"
    echo "  format     - Format code with black"
    echo "  lint       - Lint code with flake8"
    echo "  typecheck  - Type check with mypy"
    echo "  test       - Run tests with pytest"
    echo ""
    echo "Dependencies installed:"
    echo "  • Python $(python --version | cut -d' ' -f2)"
    echo "  • Textual $(python -c 'import textual; print(textual.__version__)' 2>/dev/null || echo 'not found')"
    echo "  • libnotify for desktop notifications"
    echo ""
  '';
}

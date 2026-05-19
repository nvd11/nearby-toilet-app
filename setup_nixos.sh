#!/bin/bash
set -e

cd /home/gateman/.openclaw/workspace
rm -rf nixos-config
git clone https://oauth2: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@github.com/nvd11/nixos-config.git
cd nixos-config

git config user.name "Alice (OpenClaw)"
git config user.email "gateman56@gmail.com"

# 1. Flake entry
cat << 'FLAKE' > flake.nix
{
  description = "Alice's Declarative NixOS Configuration for Boss";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, home-manager, ... }@inputs: {
    nixosConfigurations = {
      laptop = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        specialArgs = { inherit inputs; };
        modules = [
          ./hosts/laptop/configuration.nix
          ./modules/common.nix
          home-manager.nixosModules.home-manager
          {
            home-manager.useGlobalPkgs = true;
            home-manager.useUserPackages = true;
            home-manager.users.gateman = import ./home/gateman.nix;
          }
        ];
      };
    };
  };
}
FLAKE

# 2. Common modules
mkdir -p modules
cat << 'COMMON' > modules/common.nix
{ config, pkgs, ... }:

{
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  networking.networkmanager.enable = true;

  time.timeZone = "Asia/Shanghai";
  i18n.defaultLocale = "en_US.UTF-8";

  # TUNA & USTC Mirrors for mainland China
  nix.settings.substituters = [
    "https://mirrors.tuna.tsinghua.edu.cn/nix-channels/store"
    "https://mirrors.ustc.edu.cn/nix-channels/store"
    "https://cache.nixos.org/"
  ];
  
  # Enable Flakes
  nix.settings.experimental-features = [ "nix-command" "flakes" ];

  environment.systemPackages = with pkgs; [
    vim wget curl git htop
  ];

  users.users.gateman = {
    isNormalUser = true;
    description = "Jason";
    extraGroups = [ "networkmanager" "wheel" "video" "audio" ];
  };

  # Audio (Pipewire)
  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
  };
}
COMMON

# 3. Host specific configuration
mkdir -p hosts/laptop
cat << 'HOST' > hosts/laptop/configuration.nix
{ config, pkgs, ... }:

{
  imports = [
    ./hardware-configuration.nix
  ];

  networking.hostName = "laptop";

  # Enable Niri globally
  programs.niri.enable = true;

  system.stateVersion = "24.05";
}
HOST

cat << 'HW' > hosts/laptop/hardware-configuration.nix
# ⚠️ ALICE'S NOTE ⚠️
# Boss! When you install this on your actual laptop, please run:
# nixos-generate-config --show-hardware-config > hardware-configuration.nix
# and replace this file with the generated one!
{ config, lib, pkgs, modulesPath, ... }:
{
  imports = [ (modulesPath + "/installer/scan/not-detected.nix") ];
  boot.initrd.availableKernelModules = [ "nvme" "xhci_pci" "usb_storage" "sd_mod" ];
  boot.kernelModules = [ "kvm-intel" ];
  fileSystems."/" = { device = "/dev/disk/by-uuid/PLACEHOLDER"; fsType = "ext4"; };
}
HW

# 4. Home Manager (User space config)
mkdir -p home
cat << 'HOME_NIX' > home/gateman.nix
{ config, pkgs, ... }:

{
  home.username = "gateman";
  home.homeDirectory = "/home/gateman";
  home.stateVersion = "24.05";

  # Your Niri Desktop Suite & Tools
  home.packages = with pkgs; [
    alacritty
    fuzzel
    waybar
    swaybg
    grim
    slurp
    swappy
    networkmanagerapplet
    pavucontrol
    helvum
    google-chrome
    xfce.thunar
  ];

  # Fcitx5 Input Method
  i18n.inputMethod = {
    enabled = "fcitx5";
    fcitx5.addons = with pkgs; [ fcitx5-rime fcitx5-chinese-addons ];
  };

  # Declaratively load your exact Niri config
  xdg.configFile."niri/config.kdl".source = ./niri-config.kdl;
}
HOME_NIX

# 5. Bring in your existing niri config!
ssh -J gateman@100.115.214.26 gateman@10.0.1.3 'cat ~/.config/niri/config.kdl' > home/niri-config.kdl

# 6. Commit and Push
git add .
git commit -m "feat: Initial NixOS setup with Flakes, HM, and Boss's Niri config 💋"
git push -u origin main

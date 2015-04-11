# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "precise64"
  config.vm.synced_folder "./", "/vagrant"
  config.vm.provision :shell, :inline => "apt-get update -q && cd /vagrant && ./setup.sh"
  config.vm.network :forwarded_port, host: 5000, guest: 5000
end

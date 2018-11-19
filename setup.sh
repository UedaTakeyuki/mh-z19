sudo apt-get install python-pip git-core
sudo pip install mh_z19 pondslider incremental_counter error_counter
git clone https://github.com/UedaTakeyuki/handlers
ln -s handlers/value/sender/send2monitor/send2monitor.py
sudo sed -i "s/^enable_uart=.*/enable_uart=1/" /boot/config.txt
read -p "Would you like to reboot now?  (y/n) :" YN
if [ "${YN}" = "y" ]; then
  sudo reboot
else
  exit 1;
fi

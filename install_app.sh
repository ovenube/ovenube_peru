echo "Install frappe NodeJS dependencies . . ."
cd /home/frappe/frappe-bench/apps/frappe
yarn
echo "Install erpnext NodeJS dependencies . . ."
cd /home/frappe/frappe-bench/apps/erpnext
yarn
echo "Install ovenube_peru NodeJS dependencies . . ."
cd /home/frappe/frappe-bench/apps/ovenube_peru
yarn
echo "Build browser assets . . ."
cd /home/frappe/frappe-bench/apps/frappe
yarn production --app ovenube_peru
echo "Install frappe NodeJS production dependencies . . ."
cd /home/frappe/frappe-bench/apps/frappe
yarn install --production=true
echo "Install erpnext NodeJS production dependencies . . ."
cd /home/frappe/frappe-bench/apps/erpnext
yarn install --production=true
echo "Install ovenube_peru NodeJS production dependencies . . ."
cd /home/frappe/frappe-bench/apps/ovenube_peru
yarn install --production=true

mkdir -p /home/frappe/frappe-bench/sites/assets/ovenube_peru
cp -R /home/frappe/frappe-bench/apps/ovenube_peru/ovenube_peru/public/* /home/frappe/frappe-bench/sites/assets/ovenube_peru

# Add frappe and all the apps available under in frappe-bench here
echo "rsync -a --delete /var/www/html/assets/frappe /assets" >/rsync
echo "rsync -a --delete /var/www/html/assets/erpnext /assets" >/rsync
echo "rsync -a --delete /var/www/html/assets/ovenube_peru /assets" >>/rsync
chmod +x /rsync

rm /home/frappe/frappe-bench/sites/apps.txt
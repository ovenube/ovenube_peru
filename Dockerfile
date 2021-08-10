FROM node:14-buster-slim AS build

RUN apt-get update -y && \
  apt-get install build-essential git python2 -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/frappe/frappe-bench/sites/assets \
    && cd /home/frappe/frappe-bench \
    && echo -e "frappe\nerpnext\novenube_peru" > sites/apps.txt \
    && mkdir -p apps \
    && cd apps \
    && git clone --depth 1 https://github.com/ovenube/frappe.git -b version-12 frappe \
    && git clone --depth 1 https://github.com/ovenube/erpnext.git -b version-12 erpnext

COPY apps /home/frappe/frappe-bench/apps
COPY commands /home/frappe/frappe-bench
COPY install_app.sh /install_app

RUN chmod +x /install_app

RUN /install_app

FROM frappe/erpnext-nginx:version-12 AS ovenube-nginx

ENV TZ America/Lima

COPY --from=build /home/frappe/frappe-bench/sites/ /var/www/html/
COPY --from=build /rsync /rsync

RUN echo "ovenube_peru" >> /var/www/html/apps.txt \
    && mkdir -p /var/www/html/sites/ \
    && touch /var/www/html/sites/.build

VOLUME [ "/assets" ]

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]

FROM frappe/erpnext-worker:version-12 AS ovenube-worker

ENV TZ America/Lima

COPY --from=build /home/frappe/frappe-bench/apps /home/frappe/frappe-bench/apps
COPY commands /home/frappe/frappe-bench/commands

USER root

RUN /home/frappe/frappe-bench/env/bin/pip3 install -e /home/frappe/frappe-bench/apps/ovenube_peru
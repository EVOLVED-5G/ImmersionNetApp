

jq -r .capif_host=\"$CAPIF_HOST\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json
jq -r .capif_http_port=\"$CAPIF_HTTP_PORT\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json
jq -r .capif_https_port=\"$CAPIF_HTTPS_PORT\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json
jq -r .capif_callback_url=\"http://$CALLBACK_IP\" capif_registration.json >> tmp.json && mv tmp.json capif_registration.json



evolved5g register-and-onboard-to-capif --config_file_full_path="/usr/src/app/capif_registration.json"

tail -f /dev/null
#!/bin/bash

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

function pause(){
    read -p "Devam etmek için Enter'a basın..."
}

function nmap_scan(){
    read -p "Hedef IP veya Domain: " target
    echo -e "${GREEN}Nmap taraması başlatılıyor...${NC}"
    nmap $target
    pause
}

function whatweb_scan(){
    read -p "Hedef Site (http/https ile): " target
    echo -e "${GREEN}Whatweb çalışıyor...${NC}"
    whatweb $target
    pause
}

function curl_head(){
    read -p "Hedef Site (http/https ile): " target
    echo -e "${GREEN}HTTP başlık bilgisi alınıyor...${NC}"
    curl -I $target
    pause
}

function ping_test(){
    read -p "Hedef IP veya Domain: " target
    echo -e "${GREEN}Ping testi yapılıyor...${NC}"
    ping -c 4 $target
    pause
}

function dig_query(){
    read -p "Hedef Domain: " target
    echo -e "${GREEN}DNS sorgusu yapılıyor...${NC}"
    dig $target
    pause
}

while true; do
    clear
    echo -e "${RED}"
    echo "######  #######  #####  ######  #     #    "
    echo "#     #    #    #     # #     #  #   #     "
    echo "#     #    #          # #     #   # #      "
    echo "######     #     #####  ######     #       "
    echo "#          #    #       #          #       "
    echo "#          #    #       #          #       "
    echo "#          #    ####### #          #       "
    echo "                                            "
    echo "#####  ######  ####   ####  #    #           "
    echo "#    # #      #    # #    # ##   #           "
    echo "#    # #####  #      #    # # #  #           "
    echo "#####  #      #      #    # #  # #           "
    echo "#   #  #      #    # #    # #   ##           "
    echo "#    # ######  ####   ####  #    #           "
    echo -e "${NC}"
    echo "==== reconhub for new starters ===="
    echo "1) port scan with nmap"
    echo "2) learn web tech with whatweb"
    echo "3) http info with curl"
    echo "4) Ping"
    echo "5) DNS Check with Dig"
    echo "0) Exit"
    read -p "Seçiminiz: " secim

    case $secim in
        1)
            nmap_scan
            ;;
        2)
            whatweb_scan
            ;;
        3)
            curl_head
            ;;
        4)
            ping_test
            ;;
        5)
            dig_query
            ;;
        0)
            echo "Çıkış yapılıyor..."
            exit
            ;;
        *)
            echo "Geçersiz seçim!"
            sleep 1
            ;;
    esac
done

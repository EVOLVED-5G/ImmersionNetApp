#!/bin/bash

winpty docker exec -it $(docker ps -q -f "name=imm_netapp") bash

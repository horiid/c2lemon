# C2LEMON: C2 LEgion MONitoring
## Description
C2LEMON is a monitoring system for visualizing malicious C&C servers' activities collected with multiple sensor agents. Response data from each agent are collected to and integrated at a cloud data storage such as BoX, and users are able to download threat data. Not only you can visualize these data by reading files through the web APP server with a graphical Dashboard at each local environment, but also run monitor agent program independently, apart from the visualization server. You can find the sensor agent program at [my repository](https://github.com/horiid/C2sensor).

## Data Format
Data specification for responses from C&C server and a example are defined at /schema/cti-schema.json.
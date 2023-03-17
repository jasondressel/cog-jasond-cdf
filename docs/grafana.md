# Grafana

We are going to follow Cognite Academy Course.  Your data is contextualized but because there are several copies, when you work to consume the data you see multiple copies.  The data we used in our workshop is a subset extract of the full data within [Open Industrial Data](https://hub.cognite.com/open-industrial-data-211).

[Register for Cognite Hub](https://hub.cognite.com/welcome-to-cognite-hub-73/how-to-sign-up-for-cognite-hub-and-cognite-academy-617)

https://grafana.com/ - Register for Grafana

[Cognite Learn](https://learn.cognite.com/page/cognite-learn-catalog#role_domain-expert)
- [Introduction to CDF & Grafana](https://learn.cognite.com/introduction-to-cdf-grafana)
- [CDF & Grafana: Solving a Use Case](https://learn.cognite.com/solving-a-use-case-with-cdf-grafana)


The course guides you through building a overview dashboard using these 4 specific assets:
PT - Time series pressure (bar)
TT - Time series tempurature (celcius)

We can browse this in pemex-dev now:
Asset Name (Title)
* 23-PT-92532 (Pressure on suction side)
* 23-PT-92536 (Pressure on discharge side)
* 23-TT-92533 (Temperature on suction side)
* 23-TT-92539 (Temperature on discharge side)

## Create a Grafana Account
Go to grafana.com and create a new free account using your e-mail address (It can be your pemex email or personal)
### Launch Grafana
### Install the Cognite Plugin
- Configuration -> Plugins - Add Datasource (search for <b>Cognite Data Fusion</b>)
- Select and Install via grafana.com
- Install Cognite Data Fusion on Grafana Cloud



---?image=assets/images/identityimage.jpg&opacity=40

@title[Pitch]
# @size[0.3em](Enabling your Microsoft Identity Management solution to empower the IT Service Desk)

@snap[south-east]
@size[0.45em](@fa[wordpress] [blog.darrenjrobinson.com](https://blog.darrenjrobinson.com))
@fa[twitter] [@darrenjrobinson](https://twitter.com/darrenjrobinson)
@fa[github] [github.com/darrenjrobinson](https://github.com/darrenjrobinson/MIM-VoiceAssistant)
@snapend

---?image=assets/images/ITSupport.jpg&opacity=40
@title[The Problem]
@snap[north-west]
Microsoft Identity Manager has full visibility of managed entities (e.g Users) and all their entitlements and statuses
@snap[end]
@snap[east]
@ul
- but only the Identity Team has access
- giving fine grained visibility to your Service Desk is difficult if not near impossible
- and if you can, it's another console/tool for them to learn 
@ulend
@snapend

---?image=assets/images/ITSupport.jpg&opacity=40
@title[A Solution]
@snap[north-west]
What if the Service Desk had a Voice Assistant to query Micrsoft Identity Manager?
@snapend
@snap[east]
@ul
- and they could use their voice to query it for a defined set of information pertinent to the Service Desk
- without ever needing access to the Identity Management Platform
@ulend
@snapend

---?image=assets/images/identityimage.jpg&opacity=40

@title[Introducing The Voice Assistant for MIM]

## INTRODUCING 
### The Voice Assistant for Microsoft Identity Manager

---?image=assets/images/identityimage.jpg&opacity=40

## @size[0.45em](A demonstration of the Voice Assistant for MIM)
![Video](https://www.youtube.com/embed/SKzqzNE_bPo)

---?image=assets/images/identityimage.jpg&opacity=40

@title[Built With IoT]

### Built with an IoT Device
@ul
- OpenWRT on Seeed Studio Respeaker Core 1.0
- Python 2.7
@ulend

---?image=assets/images/identityimage.jpg&opacity=40

@title[Built With Azure Services]
### Built with Azure Services
@ul
- IoT Device & IoT Hub
- IoT Event Hub
- Azure Functions
- PowerShell
- Managed Service Identity
- Azure Key Vault
- Azure API Management
- Azure Table Storage
- Power BI
@ulend

---?image=assets/images/identityimage.jpg&opacity=40

@title[Built With Azure Congnitive Services]
### Built with Azure Cognitive Services
@ul
- Speech to Text
- Language Understanding Intelligent Service LUIS
- Text to Speech
@ulend

---?image=assets/images/identityimage.jpg&opacity=40

@title[Built With MIM]
### Built with Microsoft Identity Manager
@ul
- Microsoft Identity Manager 2016 SP1
- Lithnet MIM Service REST API
@ulend

---?image=assets/images/Architecture.png&position=right&size=55% 100%&color=#ffffff
@title[Architecture 1]
@snap[west commentary]
The IT Support Staff member speaks to the Voice Assistant
@snapend

---?image=assets/images/Architecture.png&position=right&size=55% 100%&color=#ffffff
@title[Architecture 2]
@snap[west commentary]
The Voice Assistant takes the spoken request and submits it to Azure Cognitive Services to convert the request from speech to text
@snapend

---?image=assets/images/Architecture.png&position=right&size=55% 100%&color=#ffffff
@title[Architecture 3]
@snap[west commentary-verbose]
The Voice Assistant then submits the request to an Azure Function that takes the request and sends it to Language Understanding Intelligent Service which identifies the Entity e.g. 'User' and Entitlement e.g 'Mailbox' and returns it to the Function which then queries Microsoft Identity Manager for the Entity and returns the record to the Function which identifies the value for the entitlement and generates the response text which is returned to the Voice Assistant
@snapend

---?image=assets/images/Architecture.png&position=right&size=55% 100%&color=#ffffff
@title[Architecture 4]
@snap[west commentary]
The Voice Assistant takes the response text and submits it to Azure Cognitive Services 'Text to Speech' to turn the response into audio
@snapend


---?image=assets/images/Architecture.png&position=right&size=55% 100%&color=#ffffff
@title[Architecture 5]
@snap[west commentary]
The Voice Assistant speaks the response to the IT Support Staff Member
@snapend  

---?image=assets/images/Architecture.png&position=right&size=55% 100%&color=#ffffff
@title[Architecture 6]
@snap[west commentary]
The Voice Assistant sends a summary of the interaction to IoT Hub which sends it to Stream Analytics and logs it to Azure Table Storage as well as sending it to Power BI which displays Analytics of the use of the Voice Assistant
@snapend  


---?image=assets/images/Dashboard.jpg&position=right&size=65% 65%&color=#ffffff
@title[Dashboard]
@snap[west commentary commentary-slim]
Analytics from the use of the Voice Assistant
@snapend  

---?color=#000000
@title[End]
### More information
#### [Devpost Hackathon submission](https://devpost.com/software/voice-assistant-for-microsoft-identity-manager)
@fa[wordpress] blog.darrenjrobinson.com </br>
@fa[twitter] @darrenjrobinson </br>
@fa[github] github.com/darrenjrobinson/MIM-VoiceAssistant</br>

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
@transition[none]
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
@transition[none]
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
@transition[none]
@snap[west]
@size[0.55em](@color[black](The IT Support Staff member))<br>
@size[0.55em](@color[black](speaks to the Voice Assistant))
@snapend

---?image=assets/images/Architecture.png&position=right&size=55% 100%&color=#ffffff
@title[Architecture 2]
@transition[none]
@snap[west]
@size[0.55em](@color[black](The Voice Assistant takes the spoken))<br>
@size[0.55em](@color[black](request and submits it to Azure))<br>
@size[0.55em](@color[black](Cognitive Services to convert the))<br>
@size[0.55em](@color[black](request from speech to text))<br>
@snapend

---?image=assets/images/Architecture.png&position=right&size=55% 100%&color=#ffffff
@title[Architecture 3]
@transition[none]
@snap[west]
@size[0.55em](@color[black](The Voice Assistant then submits the))<br>
@size[0.55em](@color[black](request to an Azure Function that takes))<br>
@size[0.55em](@color[black](the request and sends it to Language))<br>
@size[0.55em](@color[black](Understanding Intelligent Service which))<br>
@size[0.55em](@color[black](identifies the Entity e.g. 'User' and))<br>
@size[0.55em](@color[black](Entitlement e.g 'Mailbox' and returns))<br>
@size[0.55em](@color[black](it to the Function which then queries))<br>
@size[0.55em](@color[black](Microsoft Identity Manager for the Entity))<br>
@size[0.55em](@color[black](and returns the record to the Function))<br>
@size[0.55em](@color[black](which identifies the value for the))<br>
@size[0.55em](@color[black](entitlement and generates the response))<br>
@size[0.55em](@color[black](text which is returned to the Voice Assistant))<br>
@snapend


---?image=assets/images/Architecture.png&position=right&size=55% 100%&color=#ffffff
@title[Architecture 4]
@transition[none]
@snap[west]
@size[0.55em](@color[black](The Voice Assistant takes the))<br>
@size[0.55em](@color[black](response text and submits it))<br>
@size[0.55em](@color[black](to Azure Cognitive Services))<br>
@size[0.55em](@color[black]('Text to Speech' to turn the))<br>
@size[0.55em](@color[black](response into audio))<br>
@snapend


---?image=assets/images/Architecture.png&position=right&size=55% 100%&color=#ffffff
@title[Architecture 5]
@transition[none]
@snap[west]
@size[0.55em](@color[black](The Voice Assistant speaks the))<br>
@size[0.55em](@color[black](response to the IT Support))<br>
@size[0.55em](@color[black](Staff Member))<br>
@snapend  

---?image=assets/images/Architecture.png&position=right&size=55% 100%&color=#ffffff
@title[Architecture 6]
@transition[none]
@snap[west]
@size[0.55em](@color[black](The Voice Assistant sends a summary))<br>
@size[0.55em](@color[black](of the interaction to IoT Hub which))<br>
@size[0.55em](@color[black](sends it to Stream Analytics and logs))<br>
@size[0.55em](@color[black](it to Azure Table Storage as well as))<br>
@size[0.55em](@color[black](sending it to Power BI which displays))<br>
@size[0.55em](@color[black](Analytics of the use of the Voice Assistant))<br>
@snapend  


---?image=assets/images/Dashboard.jpg&position=right&size=65% 65%&color=#ffffff
@title[Dashboard]
@snap[west]
@size[0.55em](@color[black](Analytics from the use))<br>
@size[0.55em](@color[black](of the Voice Assistant))
@snapend  

---?color=#000000
@title[End]
### More information
#### [Devpost Hackathon submission](https://devpost.com/software/voice-assistant-for-microsoft-identity-manager)
@fa[wordpress] blog.darrenjrobinson.com </br>
@fa[twitter] @darrenjrobinson </br>
@fa[github] github.com/darrenjrobinson/MIM-VoiceAssistant</br>
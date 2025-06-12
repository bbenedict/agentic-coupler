# Agentic Coupler #

Bob Benedict

May, 2025

## Description ##

The **Agentic Coupler** came out of development project for creating long form books using Agentic AI.  [See original post on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7338249627999027201/)

I tried unsuccessfully to create a supervisor architecture and eventually settled on an agentic workflow because I couldn't get reliable routing. During the process of running experiments on various architectures, I created an Agentic Coupler 🔗 that separates routing from inference. The coupler connects (or "couples") the user request to the appropriate team member and just provides the suggestion.  

My code then used the suggestion to send the request to the team member along with any additional data or state.  I imagine this is how frameworks work behind the scenes.  I ended up with better routing success with one interesting side effect...

I was also able to explicitly define the state sent to each team member instead of relying on the supervisor set the context.  Here's why that matters.  When writing a book, some agents rely on the synopsis while others change the working draft.  Some steps also need locational context like where is this text within the chapter. The state graph became extensive reminding me of when we passed around huge context objects.

Better yet, the Agentic Coupler 🔗 also splits one request into many which are suggested for different team members.  Each team member therefore only sees requests intended for them.  LangChain did recent research on multi-agent architectures and discovered something similar.  "Remove the handoff messages from the sub-agent’s state so the assigned agent doesn’t have to view the supervisor’s routing logic. This de-clutters the sub-agent’s context window and lets it perform it’s task better." https://blog.langchain.dev/benchmarking-multi-agent-architectures/

## Benefits of Agentic coupling ##

🎁 Better control of routing

🎁 Dynamic team member specific state

🎁 User requests splitting by team member

## Sample Agentic coupling ###

```
agentic_coupler = AgenticCoupler()
agentic_coupler.add_team_member("MARKETING", "does marketing")
agentic_coupler.add_team_member("SALES", "handles sales")
agentic_coupler.add_team_member("FINANCE", "manages finances")

request = """
Start a new marketing campaign to emphasize organic materials. Have our 
sales people emphasize organic material to all new leads.  Make sure the 
controller tracks the revenue for this campaign. And finally, let's train 
all the customer support people on our organic products.
"""

team_members = agentic_coupler(request)

```

### Produced the following result ###

```
[{
    "team_member_id": "MARKETING",
    "user_request": "Start a new marketing campaign to emphasize organic materials.",
    "confidence": 0.95
},
{
    "team_member_id": "SALES",
    "user_request": "Have our sales people emphasize organic material to all new leads.",
    "confidence": 0.9
},
{
    "team_member_id": "FINANCE",
    "user_request": "Make sure the controller tracks the revenue for this campaign.",
    "confidence": 0.85
},
{
    "team_member_id": "UNKNOWN",
    "user_request": "Train all the customer support people on our organic products.",
    "confidence": 0.0
}]
```

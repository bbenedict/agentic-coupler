from agentic_coupler.agentic_coupler import AgenticCoupler

agentic_coupler = AgenticCoupler()
agentic_coupler.add_team_member("MARKETING", "creates or provides marketing materials as requested")
agentic_coupler.add_team_member("SALES", "handles all sales from new leads to closing deals")
agentic_coupler.add_team_member("FINANCE", "manages all financial accounts and processes all incoming and outgoing money")

# Set the team manager as the default for any request that can't be coupled with an existing team member
# agentic_coupler.add_team_member("TEAM_MANAGER", "makes all management decisions", True)

request = """
Start a new marketing campaign to emphasize we use only organic
materials. Have our sales people emphasize organic food and material when talking to
any new leads.  Make sure the controller adds a new account to track the revenue for 
this campaign.  And finally, let's train all the customer support people on our
organic products.
"""
coupled_team_members = agentic_coupler(request)

print(request)
for team_member in coupled_team_members:
    print(f"{team_member.user_request} -- sent to -- {team_member.team_member_id}({team_member.confidence})")

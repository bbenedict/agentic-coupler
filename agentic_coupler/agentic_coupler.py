from typing import List
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agentic_coupler.team_member import TeamMember
from agentic_coupler.user_requests import UserRequests


UNKNWON_TEAM_MEMBER = "UNKNOWN"

class AgenticCoupler():
    team_members: List[TeamMember] = []
    
    def add_team_member(self, team_member_id: str, role: str, default_team_member: bool = False):
        """Add a new team member to the coupler so that user requests can be handled by the team member.
        
        Args:
            team_member_id (str): Unique identifier for the team member
            role (str): What the the team member is responsible for
            default_team_member (bool): True if this team member should handle UNKNWON_TEAM_MEMBER requests
            
        Returns:
            TeamMember: The team member object
        """
        team_member = TeamMember(team_member_id=team_member_id, role=role, default_team_member=default_team_member)
        self.team_members.append(team_member)

    def __extract_requests(self, request: str) -> List[str]:
        """Internal method to extract individual user requests from one main request
        
        Args:
            request (str): The user's original request
            
        Returns:
            Requests: List of extracted user requests
        """
        requests_agent = Agent(
            name="Request Extractor Agent",
            model=OpenAIChat(id="gpt-4o"),
            instructions="""
            You are a helpful assistant that collects user requests and stores them in a list.
            You will be given a user's request and you will need to determine how many different requests the user has made.
            Start by evaluating each phrase or set of words one at a time.  
            If the phrase is not similar to the previous phrase, consider this a new request.
            You will then return a list of strings with each user request.

            Here's an example.

            The user has entered the following request:
            "How do I get from Tacoma to Seattle, WA? I would like to know more about the history of Pie Eating.  How much is 2 + 2?"

            The user has made three requests:
            - "How do I get from Tacoma to Seattle, WA?
            - I would like to know more about the history of Pie Eating.
            - How much is 2 + 2?

            The output should be:
            ["How do I get from Tacoma to Seattle, WA?", "I would like to know more about the history of Pie Eating.", "How much is 2 + 2?"]

            """,
            response_model=UserRequests,
            debug_mode=True       
        )
        task = f" Collect a list of individual user requests from the following: {request}"
        response: RunResponse = requests_agent.run(task)
        return response.content.user_requests

    def __call__(self, request: str) -> List[TeamMember]:
        """Internal method to evaluate a list of user requests against a list of team members to see which team member should handle the request.
        
        Args:
            request (str): The user request
            
        Returns:
            List[RequestedTeamMember]: List of requested team members with the original user request
        """

        if not len(self.team_members):
            raise ValueError("No team members. Can not process any user requests.")
        
        user_requests = self.__extract_requests(request)
        if not len(user_requests):
            raise ValueError("No user requests found.")
        
        default_team_member = next((team_member for team_member in self.team_members if team_member.default_team_member), None)

        team_member_prompt = ""
        for team_member in self.team_members:
            team_member_prompt += f"Use {team_member.team_member_id} as the team member id if the user has made a request that matches the following description:\n{team_member.role}\n"
        team_member_prompt += f"Use {UNKNWON_TEAM_MEMBER} if the user has made a request that does not match any of the above descriptions."
        
        instructions = f"""
        You're job is to look at a request made by a user and determine which team member should handle the request.  
        Each team member has a unqiue identifier and a description of what tasks the team member handles.
        Review the list of team members and match the request to the team member using the descripion.
        Determine a confidence score for your confidence selecting the team member which is a value from 0 to 1:
            - Values closer to 1 indicate a high confidence the match is correct
            - Values closer to zero indicate a low confidence
            - Return 0 if the request does not match any team member
        You should return the team member id and the description of the team member as the role, the confidence score as confidence, and also include the original user request

        For example, you have the following two team members:
        MATH_TEAM_MEMBER - solves math problems
        PHYSICS_TEAM_MEMBER - solves physics problems
         
        If the user requests "add 2 and 2 together", the response would be the following because the MATH_TEAM_MEMBER handles math problems and confidence is high this is a math problem:
            team_member_id: "MATH_TEAM_MEMBER",
            role: "solves math problems",
            user_request: "add 2 and 2 together"
            confidence: 0.95

        Here is the list of team members:

        {team_member_prompt}

        """

        coupling_agent = Agent(
            name="Coupling Agent",
            model=OpenAIChat(id="gpt-4o"),
            instructions=instructions,
            response_model=TeamMember,
            debug_mode=True 
        )
        
        coupled_team_members = []
        for user_request in user_requests:
            task = f"Determine which team member should handle the following user request: {user_request}"
            response: RunResponse = coupling_agent.run(task)
            team_member = response.content

            if team_member.team_member_id == UNKNWON_TEAM_MEMBER and default_team_member:
                team_member.team_member_id = default_team_member.team_member_id

            coupled_team_members.append(team_member)

        return coupled_team_members

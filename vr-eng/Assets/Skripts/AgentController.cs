using CsvHelper.Configuration.Attributes;
using System;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// This class represents an AgentController.
/// The AgentController controls one agent in the large model and the corresponding agent in the small model.
/// The positions of the agent are read from a CSV file.
/// Script should be assigned to the large agent (NavMeshAgent) in the large model.
/// </summary>
public class AgentController : MonoBehaviour
{
    /// <summary>
    /// This class represents the movement data from an Agent that is read from the CSV file.
    /// Specifically, a path is described with start time, start point (location) and destination (location).
    /// </summary>
    // TODO Move to separated script
    public class AgentMovementData
    {
        [Name("minutes_from_start")]
        public int MinutesFromStart { get; set; }

        [Name("start")]
        public string Start { get; set; }

        [Name("target")]
        public string target { get; set; }
    }

    public string csvFile; // Name of the CSV to be read(including extension). Must be located on Hololens in LocalState.In Windows under Documents/MVP Data
    public Renderer skinnedMeshRenderer; // Mesh Renderer of large Agent. Is deactivated if agent is inactive and should be hidden
    public GameObject largeModel; // Reference to the larger model in which the large agents run.
    public GameObject smallModel; // Reference to the small model in which the small agents run.
    public GameObject smallAgent; // Reference to the corresponding small agent in the small model, which is to mimic the movements of the large agent.
    private UnityEngine.AI.NavMeshAgent agent; // Large NavMesh Agent in large Modell
    private Animator mAnimator; // Animator of large Agent
    private Animator smallAgentAnimator; // Animator of small Agent
    private string currentTarget; // Name of the current target to which the Agent should run. Corresponds to a target object in the large model
    private List<AgentMovementData> agentMovementDataList = new List<AgentMovementData>(); // List of AgentMovementData describing the walking paths of an agent.
    private int currentTimeStepIndex = 0; // Index in list agentMovementDataList. Specifies which path within the list should be run next

    /// <summary>
    /// This function is called when the game starts and is responsible for initializing various components and loading data.
    /// </summary>
    private void Start()
    {
        // Get the NavMeshAgent component attached to this game object.
        agent = GetComponent<UnityEngine.AI.NavMeshAgent>();
        agent.enabled = true;
        skinnedMeshRenderer.enabled = true;

        // Load data from a CSV file using the LoadCSVData function.
        LoadCSVData(csvFile);
        if (agentMovementDataList == null || agentMovementDataList.Count == 0)
        {
            Debug.LogError("AgentMovementData konnte nicht aus CSV geladen werden " + gameObject.name);
        }
        else
        {
            agent.stoppingDistance = 1.0f;
            Debug.Log("AgentMovementData wurden aus CSV geladen. Länge: " + agentMovementDataList.Count);
        }

        if (agent == null)
        {
            Debug.LogError("The nav mesh agent component is not attached to " + gameObject.name);
        }

        mAnimator = GetComponent<Animator>();
        if (mAnimator == null)
        {
            Debug.LogError("The animator component is not attached to " + gameObject.name);
        }

        smallAgentAnimator = smallAgent.GetComponent<Animator>();
        if (smallAgentAnimator == null)
        {
            Debug.LogError("The animator component is not attached to " + smallAgent.name);
        }

        // Add listeners for time and speed change events from the TimeManager instance.
        TimeManager.instance.timeChangeEvent.AddListener(OnTimeChange);
        TimeManager.instance.speedRampFactorChangeEvent.AddListener(OnSpeedRampFactorChange);
    }

    /// <summary>
    /// This function is called once per frame and contains the logic for updating the behavior of the game object.
    /// </summary>
    private void Update()
    {

        // Check if the smallAgent is active
        if (smallAgent.activeSelf)
        {
            // Calculate the position and rotation of the large ggent (this object) relative to the largeModel
            Vector3 position = largeModel.transform.InverseTransformPoint(this.transform.position);
            Quaternion rotation = Quaternion.Inverse(largeModel.transform.rotation) * this.transform.rotation;

            // Update the smallAgent's position and rotation based on the calculated values
            smallAgent.transform.position = smallModel.transform.TransformPoint(position);
            smallAgent.transform.rotation = smallModel.transform.rotation * rotation;
        }

        // Check if there are remaining movement steps in the agentMovementDataList
        if (currentTimeStepIndex < agentMovementDataList.Count)
        {
            // Check if it's time to execute the next movement step based on the TimeManager.Compare current time (TimeManager) with next start time of a path
            if (TimeManager.instance.CurrentTime >= agentMovementDataList[currentTimeStepIndex].MinutesFromStart)
            {
                // Enable the agent and set the smallAgent and skinnedMeshRenderer to be active
                agent.enabled = true;
                smallAgent.SetActive(true);
                skinnedMeshRenderer.enabled = true;

                // Move the agent to the specified target
                MoveAgent(agentMovementDataList[currentTimeStepIndex].target);
                currentTimeStepIndex++;
            }
        }

        // Check if the agent is enabled
        if (agent.enabled == true)
        {
            // Check if the agent has reached its destination based on remaining distance whether the path is not pending
            if (agent.remainingDistance <= 2f && !agent.pathPending)
            {
                // Trigger animations to stop walking for the agent and smallAgent
                mAnimator.SetTrigger("TriggerStopWalking");
                smallAgentAnimator.SetTrigger("TriggerStopWalking");

                // Check if the current target is "Übergang"
                // All agents that leave the institute run to the "Übergang" and should be hidden afterwards.
                if (currentTarget == "Übergang")
                {
                    // Disable the agent and hide the skinnedMeshRenderer and smallAgent
                    agent.enabled = false;
                    skinnedMeshRenderer.enabled = false;
                    smallAgent.SetActive(false);
                }

            }
        }
    }

    /// <summary>
    /// Move the agent towards a specified target.
    /// </summary>
    /// <param name="target">The name of the target to move towards.</param>
    private void MoveAgent(string target)
    {
        // Enable the agent for movement
        agent.enabled = true;

        // Find the GameObject with the specified target name
        // TODO Find Object with dictionary and not with expensive function GameObject.Find()
        GameObject targetObject = GameObject.Find(target);
        if (targetObject != null)
        {
            // Get the target's position
            Vector3 targetPosition = targetObject.transform.position;

            // Set the agent's destination to the target position
            agent.SetDestination(targetPosition);

            // Trigger the walking animation for the agent and smallAgent
            mAnimator.SetTrigger("TriggerStartWalking");
            smallAgentAnimator.SetTrigger("TriggerStartWalking");

            // Update the current target
            currentTarget = target;
        }
        else
        {
            Debug.LogWarning("Objekt mit dem Namen " + target + " konnte nicht gefunden werden! Agent bewegt sich nicht");
        }
    }

    /// <summary>
    /// Load CSV data from a file and parse it into a list of AgentMovementData objects.
    /// </summary>
    /// <param name="csvFile"> Name of the CSV to be read(including extension). Must be located on Hololens in LocalState.In Windows under Documents/MVP Data. See FileInteraction script for more Information</param>
    private async void LoadCSVData(string csvFile)
    {
        try
        {
            string csvData = await FileInteraction.Load(csvFile);
            string[] lines = csvData.Split('\n');
            for (int i = 1; i < lines.Length - 1; i++)
            {
                string line = lines[i];
                string[] values = line.Split(',');
                AgentMovementData agentMovementData = new AgentMovementData
                {
                    MinutesFromStart = int.Parse(values[1].Trim()),
                    Start = values[2].Trim(),
                    target = values[3].Trim()
                };
                agentMovementDataList.Add(agentMovementData);
            }
        }

        catch (Exception e)
        {
            Debug.LogError("Fehler beim Laden der CSV-Daten:" + csvFile + ": " + e.Message);
        }
    }

    /// <summary>
    /// Handle the event when the game time changes.
    /// </summary>
    /// <param name="currentTime">The current game time.</param>
    public void OnTimeChange(float currentTime)
    {
        Debug.Log("Time Change Event");

        // Find the corresponding index for the given time
        int newIndex = FindIndexForTime(currentTime);
        if (newIndex >= 0)
        {
            // Update the current index and move the agent to the corresponding target
            currentTimeStepIndex = newIndex;

            // Get the target for the current time step
            string target = agentMovementDataList[currentTimeStepIndex].target;
            currentTarget = target;

            // Find the GameObject with the target name
            // TODO Find Object with dictionary and not with expensive function GameObject.Find()
            GameObject targetObject = GameObject.Find(target);
            if (targetObject != null)
            {
                // Get the target's position
                Vector3 targetPosition = targetObject.transform.position;

                // set the agent position directly to the target position
                transform.position = targetPosition;
                mAnimator.SetTrigger("TriggerStopWalking");
                smallAgentAnimator.SetTrigger("TriggerStopWalking");

                // If the target is "Übergang" deactivate large and small agents
                if (currentTarget == "Übergang")
                {
                    skinnedMeshRenderer.enabled = false;
                    smallAgent.SetActive(false);
                }
                else
                {
                    skinnedMeshRenderer.enabled = true;
                    smallAgent.SetActive(true);
                    agent.enabled = true;
                }
            }
            else
            {
                Debug.LogWarning("Objekt mit dem Namen " + target + " konnte nicht gefunden werden! Agent bewegt sich nicht");
            }

        }
    }

    /// <summary>
    /// Find the index in the agentMovementDataList for a given time.
    /// </summary>
    /// <param name="currentTime">The current game time.</param>
    /// <returns>The index of the time step in the agentMovementDataList.</returns>
    private int FindIndexForTime(float currentTime)
    {
        for (int i = 0; i < agentMovementDataList.Count; i++)
        {
            if (agentMovementDataList[i].MinutesFromStart > currentTime)
            {
                // Return the previous index when the time is greater than the current time
                return i - 1; 
            }
        }
        // If no matching time is found, return the index of the last entry in the list
        return agentMovementDataList.Count - 1;
    }

    /// <summary>
    /// Handle the event when the speed ramp factor changes.
    /// </summary>
    /// <param name="speedRampFactor">The new speed ramp factor value.</param>
    public void OnSpeedRampFactorChange(float speedRampFactor)
    {
        // TODO: Set speed based on the speedRampFactor
        // Set the agent's speed to 1 when the speedRampFactor is less than or equal to 2
        if (speedRampFactor <= 2f)
        {
            agent.speed = 1;
        }
        if (speedRampFactor >= 2f)
        {
            // Set the agent's speed to 3 when the speedRampFactor is greater than or equal to 2
            agent.speed = 3;
        }
    }
}
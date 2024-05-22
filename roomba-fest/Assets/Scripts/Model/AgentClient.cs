using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class AgentClient : MonoBehaviour
{
    public float agentSpeed = 1.0f;
    public Vector3 GetAgentData()
    {
        Agent a = AgentAPIHelper.GetData();
        return new Vector3(a.x, a.y, a.z);
    }


    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        var step = agentSpeed * Time.deltaTime; // calculate distance to move
        transform.position = Vector3.MoveTowards(transform.position, GetAgentData(), step);
    }
}
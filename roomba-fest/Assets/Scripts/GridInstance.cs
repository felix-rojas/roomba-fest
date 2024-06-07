using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridInstance : MonoBehaviour
{
    public GameObject web;
    int height, width
    string[] initgrid;
    // Start is called before the first frame update
    void Start()
    {
        initgrid = web.GetComponent<WebClient>().Grid;
        height = (int) initgrid[0];
        width = (int) initgrid[1];
        for int i=0; i< height; i++{
            for int j=0; j< width; j++{
                if(initgrid[i+j*i] == "X"){
                    //Instance wall vector 3d(i, j,0)
                }
                if(initgrid[i+j*i] == "P"){
                    //Instance papelero
                }
                if(initgrid[i+j*i] == "X"){
                    //Instance wall
                }
        }
    }
}

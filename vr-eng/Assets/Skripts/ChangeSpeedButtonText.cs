using Microsoft.MixedReality.Toolkit.UI;
using TMPro;
using UnityEngine;

/// <summary>
/// This script changes the text of a TextMeshPro component when an Interactable button is clicked.
/// </summary>
public class ChangeSpeedButtonText : MonoBehaviour
{
    public Interactable button; // The Interactable button that triggers the text change.
    private bool isOn = false; // A boolean to track the state of the button.
    public TextMeshPro textMesh; // The TextMeshPro component to update.

    /// <summary>
    /// Called when the script starts.
    /// </summary>
    private void Start()
    {
        // Add a listener to the button's OnClick event to handle text changes.
        button.OnClick.AddListener(ChangeText);
    }

    /// <summary>
    /// Changes the text of the associated TextMeshPro component when the button is clicked.
    /// </summary>
    private void ChangeText()
    {
        isOn = !isOn; // Toggle the state of the button.

        // Update the TextMeshPro text based on the button state.
        if (isOn)
        {
            textMesh.text = "Speed is on";
        }
        else
        {
            textMesh.text = "Speed is off";
        }

    }
}

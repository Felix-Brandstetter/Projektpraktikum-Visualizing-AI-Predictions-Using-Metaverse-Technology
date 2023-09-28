using Microsoft.MixedReality.Toolkit.UI;
using UnityEngine;

/// <summary>
/// This script is used to toggle the visibility of a GameObject using an Interactable button.
/// </summary>
public class ObjectToggle : MonoBehaviour
{
    public GameObject objectToToggle; // The GameObject to toggle visibility.
    public Interactable toggleButton; // The Interactable button used for toggling.

    /// <summary>
    /// Called when the script starts.
    /// </summary>
    private void Start()
    {
        // Add a listener to the button's OnClick event to handle the toggle action.
        toggleButton.OnClick.AddListener(ToggleObject);
    }

    /// <summary>
    /// Toggles the visibility of the associated GameObject.
    /// </summary>
    private void ToggleObject()
    {
        // Toggle the active state of the associated GameObject.
        objectToToggle.SetActive(!objectToToggle.activeSelf);
    }
}


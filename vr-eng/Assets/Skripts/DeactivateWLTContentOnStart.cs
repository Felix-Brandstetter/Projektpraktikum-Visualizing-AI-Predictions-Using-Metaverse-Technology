using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.SpatialAwareness;
using UnityEngine;

/// <summary>
///  Deactivates a specified GameObject (WLT-Content) on start and toggles spatial awareness mesh display options.
/// </summary>
public class DeactivateWLTContentOnStart : MonoBehaviour
{
    public GameObject wltContent; // The GameObject to deactivate on start.
    private IMixedRealitySpatialAwarenessMeshObserver observer; // Declaration of the Mesh Observer.
    private SpatialAwarenessMeshDisplayOptions defaultOption; // The default spatial awareness mesh display option.

    /// <summary>
    /// Awake is called when the script instance is being loaded.
    /// </summary>
    void Awake()
    {
        // Ensure that the WLT content is initially active (enabled) to map the virtual model with the real institute.
        wltContent.SetActive(true);
    }

    /// <summary>
    /// Start is called before the first frame update.
    /// </summary>
    void Start()
    {

        // Deactivate the WLT content on start.
        wltContent.SetActive(false);

        // Get the Spatial Awareness Mesh Observer from the Core Services.
        observer = CoreServices.GetSpatialAwarenessSystemDataProvider<IMixedRealitySpatialAwarenessMeshObserver>();

        // Store the default spatial awareness mesh display option.
        defaultOption = observer.DisplayOption;

    }

    /// <summary>
    /// Update is called once per frame.
    /// </summary>
    void Update()
    {
        // If the WLT content is active, set the mesh display option to None (hide mesh).
        // TODO Find out why it is not working. Walls are "transparent" (None), even if wlt-content is disabled
        if (wltContent.activeSelf)
        {
            observer.DisplayOption = SpatialAwarenessMeshDisplayOptions.None;
            Debug.Log("SpatialAwarenessMeshDisplayOptions: None");
        }
        else
        {
            // If the WLT content is inactive, restore the default mesh display option.
            Debug.Log("SpatialAwarenessMeshDisplayOptions: Occlusion");
            observer.DisplayOption = defaultOption;
        }
    }
}


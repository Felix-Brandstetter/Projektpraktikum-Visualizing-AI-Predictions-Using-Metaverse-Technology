using UnityEngine;

/// <summary>
/// A script to track the position of the Player (HoloLens) and transform the position in the small Model.
/// </summary>
public class TrackMainCameraInSmallModel : MonoBehaviour
{

    public GameObject myAgent; // Reference to the object representing the player (HoloLens).
    public GameObject largeModel; // Reference to the larger model.
    public GameObject smallModel; // Reference to the smaller model.
    private Quaternion newRotation; // The new rotation to be applied to the player's object.

    /// <summary>
    /// 
    /// </summary>
    void Start()
    {
        newRotation = Quaternion.Inverse(myAgent.transform.rotation);
    }

    /// <summary>
    /// 
    /// </summary>
    void Update()
    {
        // Calculate the position in the local space of the large model.
        Vector3 position = largeModel.transform.InverseTransformPoint(transform.position);

        // Adjust the z-coordinate of the position to account for the difference.
        position.z -= 1.6f;

        // Transform the adjusted position to the small model's coordinate space.
        myAgent.transform.position = smallModel.transform.TransformPoint(position);

        // Corrected rotation assignment to only rotate around the y-axis.
        newRotation.eulerAngles = new Vector3(0f, this.transform.rotation.eulerAngles.y, 0f);

        // Apply the corrected rotation to the player's object.
        myAgent.transform.rotation = newRotation.normalized;
    }
}

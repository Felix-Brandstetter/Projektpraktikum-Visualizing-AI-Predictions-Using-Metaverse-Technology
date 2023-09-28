using UnityEngine;

/// <summary>
///  Manages game time and provides events for time and speed ramp factor changes.
///  Time starts Mondays at 8:00 am and runs until 6:00 pm. A TimeIndex (time) of 601 corresponds to Tuesday at 8:01 am.
/// </summary>
public class TimeManager : MonoBehaviour
{
    public static TimeManager instance; // Singleton instance
    public TimeChangeEvent timeChangeEvent; // Event for time changes
    public SpeedRampFactorChangeEvent speedRampFactorChangeEvent; // Event for speed ramp factor changes

    // Private fields to manage time and speed ramp factor
    private float _speedRampFactor = 1f;
    private float _previousTime;
    private float _currentTime;
    private float _selectedTime;
    private bool _speedRampFactorActive;
    private float time;

    // Properties to access time and speed ramp factor
    public float CurrentTime
    {
        get => _currentTime;
        set
        {
            _currentTime = value;
            timeChangeEvent.Invoke(_currentTime);
            Debug.Log("Time changed to " + _currentTime);
        }
    }

    public float SelectedTime
    {
        get => _selectedTime;
        set => _selectedTime = value;
    }

    public float SpeedRampFactor
    {
        get => _speedRampFactor;
        set
        {
            _speedRampFactor = value;
            speedRampFactorChangeEvent.Invoke(_speedRampFactor);
            Debug.Log("SpeedRampFactor  changed to " + _speedRampFactor);
        }
    }

    /// <summary>
    /// Awake is called when the script instance is being loaded.
    /// </summary>
    private void Awake()
    {
        // Singleton pattern setup
        if (instance != null && instance != this)
        {
            Destroy(this.gameObject);
        }
        else
        {
            instance = this;
            timeChangeEvent = new TimeChangeEvent(); // Create an instance of TimeChangeEvent
            speedRampFactorChangeEvent = new SpeedRampFactorChangeEvent();
            DontDestroyOnLoad(this.gameObject);
        }
    }

    /// <summary>
    /// Called when the script starts.
    /// </summary>
    private void Start()
    {
        _currentTime = 0.0f;
    }

    /// <summary>
    /// Called once per frame to update gametime
    /// </summary>
    private void Update()
    {

        // Calculate the time difference since the last update
        time = Time.time;
        float deltaTime = time - _previousTime;
        _previousTime = time;

        // If the SpeedRampFactor is active, multiply the deltaTime by the factor
        float modifiedDeltaTime = deltaTime * _speedRampFactor;

        // Add the modified time difference to the current time
        _currentTime += modifiedDeltaTime / 60f;
    }

    /// <summary>
    /// Set the current time as the selected time. Used in TimeSelecter.cs
    /// </summary>
    public void SetCurrentTimeAsSelectedTime()
    {
        _currentTime = _selectedTime;
        timeChangeEvent.Invoke(_currentTime);
        Debug.Log("Time changed to " + _currentTime);

    }
    /// <summary>
    /// Activate or deactivate the SpeedRampFactor.
    /// Used for Debugging in KeyInputListener.cs
    /// </summary>
    /// <param name="speedRampFactor">The speed ramp factor to activate or deactivate.</param>
    public void activateDeactivateSpeedRampFactor(float speedRampFactor)
    {
        // TODO: Make the SpeedRampFactor explicitly adjustable. You could select values using a slider in the HandMenu.
        if (!_speedRampFactorActive)
        {
            _speedRampFactor = speedRampFactor;
            Debug.Log("SpeedRampFactor  changed to " + _speedRampFactor);
            speedRampFactorChangeEvent.Invoke(_speedRampFactor);
            _speedRampFactorActive = true;
        }
        else
        {
            _speedRampFactor = 1f;
            Debug.Log("SpeedRampFactor  changed to " + _speedRampFactor);
            _speedRampFactorActive = false;
            speedRampFactorChangeEvent.Invoke(_speedRampFactor);
        }
    }
}



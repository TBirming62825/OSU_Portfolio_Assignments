import { useState } from 'react';   // React hook for state management
import { useNavigate } from 'react-router-dom'; // React Router hook for navigation

export const CreatePage = () => {

    // State declarations - Keeps track of "state" in form fields
    // JS: storing values in variables and reading them from the DOM
    const [name, setName] = useState('');
    const [reps, setReps] = useState('');
    const [weight, setWeight] = useState('');
    const [unit, setUnit] = useState('');
    const [date, setDate] = useState('');

    const navigate = useNavigate(); // used to navigate to a new page after submit

    // Event handler for form submission
    const addExercise = async (e) => {
        e.preventDefault(); // prevent the default form submission behavior
                            // Equivalent in JS: event.preventDefault()

        // Collect form data
        // React: state variables contain current user input
        // JS: you'd read from input elements using .value
        const newExercise = {name, reps, weight, unit, date}

        // Send data to server
        // React: using fetch API
        // JS: exactly the same — you would fetch('/exercises', {...})
        const response = await fetch(
                '/exercises', {   
                method: 'POST',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(newExercise)
            }
        );

        // Handle server response
        // JS: Same as checking response
        if(response.status === 201){
            alert('Exercise successfully logged. Great work, keep it up!')
        }else{
            alert(`Exercise upload failed. Status Code: ${response.status}`)
        }
        
        // Navigate to another page
        // React Router
        // JS: window.location.href = '/'
        navigate('/') 
    };

    // JSX render
    return (
        <div>
            <form onSubmit={addExercise}>
                <fieldset>
                    <legend>Add an Exercise</legend>
                        {/* -----------------------------
                            Inputs bound to state
                            -----------------------------
                            React: value={stateVar} + onChange updates state
                            JS: you'd read/write input.value directly and use addEventListener
                        ----------------------------- */}
                        <p>
                            <label>Enter Name:
                                <input
                                    type="text"
                                    placeholder="Exercise name"
                                    value={name}
                                    onChange={e => setName(e.target.value)} /> {/* update state */}
                            </label>
                        </p>
                        <p>
                            <label>Enter reps:
                                <input
                                    type="number"
                                    value={reps}
                                    placeholder="Rep count"
                                    onChange={e => setReps(e.target.valueAsNumber)} /> {/* convert to number */}
                            </label>
                        </p>
                        <p>
                            <label>Enter Weight:
                                <input
                                    type="number"
                                    placeholder="Weight"
                                    value={weight}
                                    onChange={e => setWeight(e.target.valueAsNumber)} />
                            </label>
                        </p>
                        <p>
                            <label>Enter Units:
                                <select value={unit} onChange={e => setUnit(e.target.value)}>
                                    <option value="">Select...</option>
                                    <option value="lbs">lbs</option>
                                    <option value="kgs">kgs</option>
                                    <option value="miles">miles</option>
                                </select>
                            </label>
                        </p>
                        <p>
                            <label>Enter Workout Date:
                                <input
                                    type="date"
                                    value={date}
                                    onChange={e => setDate(e.target.value)} />
                            </label>
                        </p>
                </fieldset>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default CreatePage;
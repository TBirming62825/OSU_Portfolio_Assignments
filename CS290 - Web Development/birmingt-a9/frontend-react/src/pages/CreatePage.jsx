import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const CreatePage = () => {

    const [name, setName] = useState('');
    const [reps, setReps] = useState('');
    const [weight, setWeight] = useState('');
    const [unit, setUnit] = useState('');
    const [date, setDate] = useState('');

    const navigate = useNavigate();

    const addExercise = async (e) => {
        e.preventDefault();

        const newExercise = {name, reps, weight, unit, date}
        const response = await fetch(
                '/exercises', {   
                method: 'POST',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(newExercise)
            }
        );

        if(response.status === 201){
            alert('Exercise successfully logged. Great work, keep it up!')
        }else{
            alert(`Exercise upload failed. Status Code: ${response.status}`)
        }

        navigate('/')
    };

    return (
        <div>
            <form onSubmit={addExercise}>
                <fieldset>
                    <legend>Add an Exercise</legend>
                        <p>
                            <label>Enter Name:
                                <input
                                    type="text"
                                    placeholder="Exercise name"
                                    value={name}
                                    onChange={e => setName(e.target.value)} />
                            </label>
                        </p>
                        <p>
                            <label>Enter reps:
                                <input
                                    type="number"
                                    value={reps}
                                    placeholder="Rep count"
                                    onChange={e => setReps(e.target.valueAsNumber)} />
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
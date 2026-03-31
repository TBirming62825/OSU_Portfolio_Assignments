import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const UpdatePage = ({exerciseToEdit}) => {

    const [name, setName] = useState(exerciseToEdit.name);
    const [reps, setReps] = useState(exerciseToEdit.reps);
    const [weight, setWeight] = useState(exerciseToEdit.weight);
    const [unit, setUnit] = useState(exerciseToEdit.unit);
    const [date, setDate] = useState(exerciseToEdit.date?.split('T')[0]);

    const navigate = useNavigate();

    const editExercise = async (e) => {
        e.preventDefault();

        const editedExercise = {name, reps, weight, unit, date}
        const response = await fetch(
                `/exercises/${exerciseToEdit._id}`, {   
                method: 'PUT',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(editedExercise)
            }
        );

        if(response.status === 200){
            alert('Exercise successfully edited. Way to go!')
        }else{
            alert(`Exercise edit request failed. Status Code: ${response.status}`)
        }

        navigate('/')
    };

    return (
        <div>
            <form onSubmit={editExercise}>
                <fieldset>
                    <legend>Edit your Exercise</legend>
                        <p>
                            <label>Enter Name:
                                <input
                                    type="text"
                                    value={name}
                                    onChange={e => setName(e.target.value)} />
                            </label>
                        </p>
                        <p>
                            <label>Enter reps:
                                <input
                                    type="number"
                                    value={reps}
                                    onChange={e => setReps(e.target.valueAsNumber)} />
                            </label>
                        </p>
                        <p>
                            <label>Enter Weight:
                                <input
                                    type="number"
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
                <button type="submit">Update</button>
            </form>
        </div>
    );
}

export default UpdatePage;
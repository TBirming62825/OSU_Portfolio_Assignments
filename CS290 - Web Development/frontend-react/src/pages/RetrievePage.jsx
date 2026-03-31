import ExerciseTable from '../components/ExerciseTable';
import { useEffect, useState} from 'react';
import { useNavigate } from 'react-router-dom';

function RetrievePage({setExerciseToEdit}) {
    const [exercises, setExercises] = useState([]);

    const navigate = useNavigate();

    const loadExercises = async () => {
        const response = await fetch('/exercises')
        const data = await response.json();
        setExercises(data)
    }

    useEffect( () => {
        loadExercises()
        }, []);

    const onDelete = async (_id) =>{
        const response = await fetch(
            `/exercises/${_id}`,
            {method: 'DELETE'}
        );
        if(response.status === 204){
            setExercises(exercises.filter(exercise => exercise._id !== _id ))
        } else {
            alert(`Deleting exercise with _id ${_id} failed. Status Code: ${response.status}`)
        }
    }

    const onEdit = (exercise) =>{
        setExerciseToEdit(exercise)
        navigate('/update-page')
    }

    return (
        <>
            <h2>Completed Exercises</h2>
            <ExerciseTable exercises={exercises} onDelete={onDelete} onEdit={onEdit}></ExerciseTable>
        </>
    );
}

export default RetrievePage;
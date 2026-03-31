import '../App.css';
import { IoIosCloseCircleOutline } from "react-icons/io";
import { IoIosConstruct } from "react-icons/io";

function ExerciseRow({ exercise, onDelete, onEdit}) {

    return (
            <tr>
                <td className="deleteButton" onClick={() => onDelete(exercise._id)}><IoIosCloseCircleOutline/> </td>
                <td>{exercise.name}</td>
                <td>{exercise.reps}</td>
                <td>{exercise.weight}</td>
                <td>{exercise.unit}</td>
                <td>{exercise.date?.split('T')[0]}</td>
                <td className="editButton" onClick={() => onEdit(exercise)}><IoIosConstruct/></td>
            </tr>

    );
}

export default ExerciseRow;
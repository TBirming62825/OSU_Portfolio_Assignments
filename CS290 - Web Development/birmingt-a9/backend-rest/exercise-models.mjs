// Get the mongoose object
import mongoose from 'mongoose';
import 'dotenv/config';

const EXERCISES_CLASS = 'Exercises'

let connection = undefined;
let Exercise = undefined;

/**
 * This function connects to the MongoDB server.
 */
async function connect(){
    try{
        await mongoose.connect(process.env.MONGODB_CONNECT_STRING);
        connection = mongoose.connection;
        console.log("Successfully connected to MongoDB using Mongoose!");

        Exercise = createModel();

    } catch(err){
        console.log(err);
        throw Error(`Could not connect to MongoDB ${err.message}`)
    }
}

function createModel(){
    // Defines schema
    const exercisesSchema = mongoose.Schema({
        name: {type: String, required: true},                   // The name of the exercise.
        reps: {type: Number, required: true},                   // The number of times the exercise was performed, or the distance. The value must be an integer greater than 0.
        weight: {type: Number, required: true},                 // The amount of the weight used for the exercise. The value must be an integer equal to or greater than 0.
        unit: {type: String, required: true},                   // The unit of measurement of the weight or the reps. Values are kgs,  lbs, and miles.
        date: {type: Date, default: Date.now, required: true},  // The date the exercise was performed. Specified as the ISO string for date and time. Set the default to Date.now.
    }, {collection:'exercises'});
    // Compile the model class from the schema
    return mongoose.model(EXERCISES_CLASS, exercisesSchema);
}

// Create exercises
async function createExercise(name, reps, weight, unit, date){
    const exercise = new Exercise({name: name,
                        reps: reps,
                        weight: weight,
                        unit: unit,
                        date: date})
    return exercise.save();
}

// Find all exercises
async function findExercises(filter){
    const query = Exercise.find(filter);
    return query.exec();
}

// Find an exercise by its ID
async function findExerciseId(exerciseId){
    const query = Exercise.findById(exerciseId);
    return query.exec();
}

// Update an exercises by its ID
async function updateExerciseId(exerciseId, body){
    const updateExercise = await Exercise.updateOne({_id: exerciseId}, body)
    if (updateExercise.matchedCount){
        return findExerciseId(exerciseId)
    }
}

// Delete an exercise by its ID
async function deleteExerciseId(exerciseId){
    const accountDelete = await Exercise.deleteOne({_id: exerciseId});
    return accountDelete.deletedCount;
}

export { connect, createExercise, findExercises, findExerciseId, updateExerciseId, deleteExerciseId};
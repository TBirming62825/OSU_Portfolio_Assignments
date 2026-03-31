import 'dotenv/config';
import express from 'express';
import asyncHandler from 'express-async-handler';
import { body, validationResult } from "express-validator"
import * as exercises from './exercise-models.mjs';

const PORT = process.env.PORT;

const app = express();
app.use(express.json())

// Connect to the server
app.listen(PORT, async () => {
    await exercises.connect(false)
    console.log(`Server listening on port ${PORT}...`);
});

// Create a new exercise
app.post('/exercises', [
    body("name").exists().notEmpty(),                       // Check that name exists and is not empty
    body("reps").exists().isInt({ min: 1 }),                // Check that reps exists and is greater than or equal to 1
    body("weight").exists().isInt({ min: 0 }),              // Check that weight exists and is greater than or equal to 0
    body("unit").exists().isIn(["kgs", "lbs", "miles"]),    // Check that unit exists and is "kgs", "lbs", or "miles"
    body("date").optional().custom((date) => {              // If date exists, check that it is the correct format
        if (isNaN(Date.parse(date))){
            throw new Error()
        } else {
            return true
        }})
    ], asyncHandler(async (request, response) => {
    const expressValidation = validationResult(request);
    if (expressValidation.isEmpty()){
        const newExercise = await exercises.createExercise(request.body.name, request.body.reps, request.body.weight, request.body.unit, request.body.date)
        response.status(201).send(newExercise)
    } else {
        response.status(400).json({Error: 'Invalid Request'})
    }
}))

// Retrieve all of the exercises. Return empty array if collection is empty.
app.get('/exercises', asyncHandler(async (request, response) =>{
    const exercise = await exercises.findExercises(request.query)
    response.send(exercise)
}))

// Retrieve a specific exercise by ID
app.get('/exercises/:id', asyncHandler(async (request, response) =>{
    const exercise = await exercises.findExerciseId(request.params.id)
    if (!exercise){
        response.status(404).json({Error: 'Not found'})
    } else {
        response.send(exercise)
    }
}))

// Update a specific exercise by ID
app.put('/exercises/:id', [
    body("name").exists().notEmpty(),                       // Check that name exists and is not empty
    body("reps").exists().isInt({ min: 1 }),                // Check that reps exists and is greater than or equal to 1
    body("weight").exists().isInt({ min: 0 }),              // Check that weight exists and is greater than or equal to 0
    body("unit").exists().isIn(["kgs", "lbs", "miles"]),    // Check that unit exists and is "kgs", "lbs", or "miles"
    body("date").optional().custom((date) => {              // If date exists, check that it is the correct format
        if (isNaN(Date.parse(date))){
            throw new Error()
        } else {
            return true
        }})
    ], asyncHandler(async (request, response) => {
    const expressValidation = validationResult(request);
    if (expressValidation.isEmpty()){
        const update = await exercises.updateExerciseId(request.params.id, request.body)
        if (!update){
            response.status(404).json({Error: 'Not found'})
        } else {
            response.send(update)
        }
    } else {
        response.status(400).json({Error: 'Invalid Request'})
    }
}))

// Delete a specific exercise by ID
app.delete('/exercises/:id', asyncHandler(async (request, response) =>{
    const exercise = await exercises.deleteExerciseId(request.params.id)
    if (exercise === 0){
        response.status(404).json({Error: 'Not found'})
    } else {
        response.status(204).send()
    }
}))
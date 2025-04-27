const response = {
    insertDoc: { message: "document inserted successfully", code: 200 },
    updateDoc: { message: "document updated successfully", code: 200 },
    readDoc: { message: "document fetched successfully", code: 200 },
    readAllDoc: { message: "documents fetched successfully", code: 200 },
    deleteDoc: { message: "document deleted successfully", code: 200 },
    insertErrorDoc: { message: "document is not inserted", code: 503 },
    updateErrorDoc: { message: "document is not updated", code: 503 },
    readErrorDoc: { message: "document is not fetched", code: 404 },
    readAllErrorDoc: { message: "documents are not fetched", code: 404 },
    deleteErrorDoc: { message: "document is not deleted", code: 503 },
    noResult: { message: "No result found!", code: 404 },
    storageError: { message: "Storage Error", code: 400 },
    validationError: { message: "Validation Error", code: 400 },
    alreadyExists: { message: "document already exists!", code: 200 },
    doesntExists: { message: "document doesnt exists!", code: 502 },
    authError: { message: "Authorisation Error", code: 511 },
    refreshError: { message: "Refresh Token Expired", code: 511 },
}

module.exports = { response }
from flask import Flask, request
app = Flask(__name__)
# Create the appropriate app.route functions. Test and see if they work

# Make an app.route() decorator here for when the client sends the URI "/puppies"


@app.route('/puppies', methods=['GET', 'POST'])
def puppiesFunction():
    if request.method == 'GET':
        # Call the method to Get all of the puppies
        return getAllPuppies()
    elif request.method == 'POST':
        return makeANewPuppy()
# Call the method to make a new puppy
# Make another app.route() decorator here that takes in an integer named 'id' for when the client visits a URI like "/puppies/5"

# DON'T include '/' in the end, it will cause errors.
@app.route('/puppies/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def puppiesFunctionId(id):
    if request.method == 'GET':
        # Call the method to get a specific puppy based on their id
        return getPuppy(id)
    elif request.method == 'PUT':
        # Call the method to update a puppy
        return updatePuppy(id)
    elif request.method == 'DELETE':
        # Call the method to remove a puppy
        return deletePuppy(id)


def getAllPuppies():
    return "Getting All the puppies!"


def makeANewPuppy():
    return "Creating A New Puppy!"


def getPuppy(id):
    return "Getting Puppy with id %s" % id


def updatePuppy(id):
    return "Updating a Puppy with id %s" % id


def deletePuppy(id):
    return "Removing Puppy with id %s" % id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

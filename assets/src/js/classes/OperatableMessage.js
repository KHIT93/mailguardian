export default class OperatableMessage {
    /**
     * Create a new Form instance.
     *
     * @param {object} data
     */
    constructor(data) {

        for (let field in data) {
            this[field] = data[field];
        }
        this['selected'] = false;
    }
}
import * as moment from 'moment';
export function bytesToHuman(value) {
    let kb = 1024;
    let mb = 1024 * 1024;
    let gb = 1024 * 1024 * 1024;
    if (value < kb) {
        return value + ' B';
    }
    else if (value >= kb && value < mb) {
        return (value / kb).toFixed(2) + ' KB';
    }
    else if (value >= mb && value < gb) {
        return (value / mb).toFixed(2) + ' MB';
    }
    else {
        return (value / gb).toFixed(2) + ' GB';
    }
}

export function timeAgo(value) {
    return moment(value).fromNow();
}

export function boolToHuman(value) {
    return value ? 'Yes' : 'No';
}
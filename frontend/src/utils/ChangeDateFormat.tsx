export const  changeDateFormat = (value: string) => {
    //from yyyy-mm-dd to dd-mm-yyyy
    if (!value) {
        return value;
    }
    //1. check if the date is correct
    if (value.length !== 10) {
        return value;
    }
    //2. check if the date is in the correct format
    if (!value.match(/^\d{4}-\d{2}-\d{2}$/)) {
        return value;
    }
    //3. split the date into parts
    const dateParts = value.split("-");
    //4. reverse the parts
    const reversedDate = dateParts.reverse();
    //5. join the parts
    const newDate = reversedDate.join("-");
    return newDate;
}
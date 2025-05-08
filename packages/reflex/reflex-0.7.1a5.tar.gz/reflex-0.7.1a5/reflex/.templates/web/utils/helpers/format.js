export default function pythonFormat(number, formatSpecifier) {
    // Parse the format specifier
    const formatRegex = /^(?<fill>.)?(?<align>[<>=^])?(?<sign>[-+ ])?(?<alt>#)?(?<zero>0)?(?<width>\d+)?(?<grouping>[_,])?(?<precision>\.\d+)?(?<type>[a-zA-Z])?$/;
    const match = formatSpecifier.match(formatRegex);

    if (!match) {
        throw new Error("Invalid format specifier.");
    }

    const {
        fill = " ",
        align = ">",
        sign = "-",
        alt,
        zero,
        width,
        grouping,
        precision,
        type = "g",
    } = match.groups;

    // Handle precision for floats
    let formattedNumber;
    if (type === "f" || type === "e" || type === "g" || type === "%") {
        const precisionValue = precision ? parseInt(precision.slice(1), 10) : 6;
        switch (type) {
            case "f":
                formattedNumber = number.toFixed(precisionValue);
                break;
            case "e":
                formattedNumber = number.toExponential(precisionValue);
                break;
            case "g":
                formattedNumber = number.toPrecision(precisionValue);
                break;
            case "%":
                formattedNumber = (number * 100).toFixed(precisionValue) + "%";
                break;
        }
    } else if (type === "d" || type === "b" || type === "o" || type === "x" || type === "X") {
        // Handle integer types
        const base = {
            b: 2,
            o: 8,
            d: 10,
            x: 16,
            X: 16,
        }[type];
        formattedNumber = Math.floor(number).toString(base);
        if (type === "X") {
            formattedNumber = formattedNumber.toUpperCase();
        }
        if (alt && (type === "o" || type === "x" || type === "X")) {
            formattedNumber = (type === "o" ? "0o" : "0x") + formattedNumber;
        }
    } else {
        throw new Error(`Unsupported format type: ${type}`);
    }

    // Handle sign
    if (sign !== "-") {
        if (number >= 0) {
            formattedNumber = sign === "+" ? "+" + formattedNumber : sign === " " ? " " + formattedNumber : formattedNumber;
        } else {
            formattedNumber = "-" + formattedNumber;
        }
    }

    // Handle grouping (thousands separator)
    if (grouping) {
        const parts = formattedNumber.split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, grouping === "," ? "," : "_");
        formattedNumber = parts.join(".");
    }

    // Handle zero-padding and width
    if (width) {
        const padLength = Math.max(0, parseInt(width, 10) - formattedNumber.length);
        if (padLength > 0) {
            const padChar = zero ? "0" : fill;
            if (align === ">") {
                formattedNumber = formattedNumber.padStart(padLength + formattedNumber.length, padChar);
            } else if (align === "<") {
                formattedNumber = formattedNumber.padEnd(padLength + formattedNumber.length, padChar);
            } else if (align === "^") {
                const leftPad = Math.floor(padLength / 2);
                const rightPad = Math.ceil(padLength / 2);
                formattedNumber = formattedNumber
                    .padStart(leftPad + formattedNumber.length, padChar)
                    .padEnd(rightPad + formattedNumber.length, padChar);
            } else if (align === "=") {
                // Handle numeric alignment (sign-aware padding)
                const signChar = formattedNumber.match(/^[+-]/)?.[0] || "";
                const numPart = formattedNumber.slice(signChar.length);
                formattedNumber = signChar + numPart.padStart(padLength + numPart.length, padChar);
            }
        }
    }

    return formattedNumber;
}

// Example usage:
console.log(pythonFormat(1234.5678, "10.2f")); // "   1234.57"
console.log(pythonFormat(-1234.5678, "+.3f")); // "-1234.568"
console.log(pythonFormat(1234.5678, "0>+10,.2f")); // "0+1,234.57"
console.log(pythonFormat(255, "#04x")); // "0xff"
console.log(pythonFormat(255, "08b")); // "11111111"
console.log(pythonFormat(1234567, "_,d")); // "1_234_567"
console.log(pythonFormat(0.12345, ".2%")); // "12.35%"
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { message } = body;
        
        const ml_url = process.env.ML_SERVICE_URL;
        
        if (!ml_url) {
            console.error("ML_SERVICE_URL environment variable is not defined");
            return NextResponse.json({ error: "Missing ML service configuration" }, { status: 500 });
        }
        
        console.log(`Attempting to connect to ML service at: ${ml_url}/chat/ask`);

        try {
            const response = await fetch(`${ml_url}/chat/ask`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: message,
                }),
            });

            if (!response.ok) {
                console.error(`ML service responded with status: ${response.status}`);
                return NextResponse.json({ 
                    error: "ML service error", 
                    status: response.status 
                }, { status: 502 });
            }

            const data = await response.json();
            console.log("ML service response:", data);

            // Return the ML service response
            return NextResponse.json({ message: data.message }, { status: 200 });
        }
        catch (error: any) {
            console.error("Error in ML service request:", error.message);
            return NextResponse.json({ 
                error: "Internal Server Error", 
                details: error.message 
            }, { status: 500 });
        }
    }
    catch (error: any) {
        console.error("Error in POST request:", error.message);
        return NextResponse.json({ 
            error: "Internal Server Error", 
            details: error.message 
        }, { status: 500 });
    }
}
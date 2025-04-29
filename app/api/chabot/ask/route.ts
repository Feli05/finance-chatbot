import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { message } = body;
        
        const ml_url = process.env.ML_SERVICE_URL;

        try {
            await fetch(`${ml_url}/chat/ask`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: message,
                }),
            });

            // Return success response after POSTing to ML service
            return NextResponse.json({ message: "ok" }, { status: 200 });
        }
        catch (error: any) {
            console.error("Error in ML service request:", error);
            return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
        }
    }
    catch (error: any) {
        console.error("Error in POST request:", error);
        return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
    }
}
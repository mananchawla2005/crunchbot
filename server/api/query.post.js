
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(useRuntimeConfig().gemini);
const embeddingModel = genAI.getGenerativeModel({ model: "models/text-embedding-004" });
const generationModel = genAI.getGenerativeModel({model: "gemini-1.5-flash"})

function irfScore(ranksList, epsilon = 0.001) {
	const irfScores = {};
	const docRanks = ranksList.map((ranks) => {
	  return ranks.map((doc, index) => ({ id: doc.id, rank: index + 1 }));
	});
  
	const allDocs = new Set(docRanks.flat().map((doc) => doc.id));
  
	allDocs.forEach((docId) => {
	  let score = 0;
  
	  docRanks.forEach((ranks) => {
		const rankEntry = ranks.find((r) => r.id === docId);
		const rank = rankEntry ? rankEntry.rank : ranks.length + 1; 
		score += 1 / (rank + epsilon);
	  });
  
	  irfScores[docId] = score;
	});
  
	return irfScores;
  }

const makePrompt = (query, relevantPassage) => {
	const escapedPassage = relevantPassage
		.replace(/'/g, "") 
		.replace(/"/g, "") 
		.replace(/\n/g, " "); 

	const prompt = `
	You are a helpful and informative bot that answers questions using text from the reference passages included below. 
	Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. 
	Be sure to add relevant example code if deduced from the relevant paragraph in markdown format.
	If the passage is irrelevant to the answer, you may ignore it.

	QUESTION: '${query}'
	PASSAGE: '${escapedPassage}'

	ANSWER:
	`;

	return prompt;
};

export default defineEventHandler(async (event) => {
	if (event.context.user) {
		const body = await readBody(event)
		const conversation = body.conversation
		const last_message = conversation.at(-1)
		const userContent = last_message.content
		const userEmbedding = await embeddingModel.embedContent({
			content: { parts: [{ text: userContent }] },
			taskType: "retrieval_query"
		})
		const embedding = userEmbedding.embedding.values
		const embeddingResponse = await pool.query("SELECT id, content, 1 - (embedding <=> $1) AS similarity FROM chunks ORDER BY similarity DESC LIMIT 20", [ JSON.stringify(embedding)])
		const searchResponse = await pool.query("SELECT id, content, ts_rank(to_tsvector('english', content), plainto_tsquery('english', $1)) AS similarity FROM chunks WHERE to_tsvector('english', content) @@ plainto_tsquery('english', $1) ORDER BY similarity DESC LIMIT 20", [userContent])
		const embeddingRows = embeddingResponse.rows
		const searchRows = searchResponse.rows
		const combinedScores = irfScore([embeddingRows, searchRows])
		const idToContent = {};
			[...embeddingRows, ...searchRows].forEach((doc) => {
			idToContent[doc.id] = doc.content
		});
		var finalRanking = Object.entries(combinedScores)
			.sort((a, b) => b[1] - a[1])
			.map(([id, score]) => ({
				id,
				content: idToContent[id],
				score: score.toFixed(4),
		}));
		finalRanking = finalRanking.slice(0, 20)
		const passages = finalRanking.map(msg=>msg.content).join("\n")
		const prompt = makePrompt(userContent, passages)
		const transformedMessages = conversation.slice(0, -1).map(msg => ({
			role: msg.role,
			parts: [{ text: msg.content ? msg.content.trim() : '' }]
		}));
		const chat = generationModel.startChat({
			history: transformedMessages
		});
		let result = await chat.sendMessage(prompt)
		return result.response.text()

	}
	else {
		throw createError({
			message: "Unauthorised Access not allowed",
			statusCode: 401
		});
    }
});


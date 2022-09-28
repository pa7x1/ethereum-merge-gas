import std/json
import std/strutils
import std/os
import std/times
import strformat

proc loadJSON(fp: string): JsonNode =
    let f = readFile(fp)
    result = parseJson(f)


proc removeTransactions(jsonBlock: JsonNode): JsonNode = 
    delete(obj=jsonBlock, key="transactions")
    return jsonBlock


func isBlockGreaterOrEqual(number: int, filepath: string): bool =
    let filename: string = splitFile(filepath).name
    let blockNumber: int = parseInt(split(s=filename, sep="_")[1])
    result = blockNumber >= number


func isBlockLessThan(number: int, filepath: string): bool =
    let filename: string = splitFile(filepath).name
    let blockNumber: int = parseInt(split(s=filename, sep="_")[1])
    result = blockNumber < number


proc loadAllJSONBlocks(dir: string, lessThan: int = -1, greaterOrEqualThan: int = -1): JsonNode =
    result = %* []
    if lessThan == -1 and greaterOrEqualThan == -1:
        for jsonFile in walkFiles(dir & "/*.json"):
            result.add(removeTransactions(loadJSON(jsonFile)))
    else:
        if lessThan == -1:
            for jsonFile in walkFiles(dir & "/*.json"):
                if isBlockGreaterOrEqual(greaterOrEqualThan, jsonFile):
                    result.add(removeTransactions(loadJSON(jsonFile)))
        elif greaterOrEqualThan == -1:
            for jsonFile in walkFiles(dir & "/*.json"):
                if isBlockLessThan(lessThan, jsonFile):
                    result.add(removeTransactions(loadJSON(jsonFile)))
        else:
            for jsonFile in walkFiles(dir & "/*.json"):
                if isBlockLessThan(lessThan, jsonFile) and isBlockGreaterOrEqual(greaterOrEqualThan, jsonFile):
                    result.add(removeTransactions(loadJSON(jsonFile)))


proc writeBlocksToFile(fp: string, blockArray: JsonNode) =
    writeFile(filename=fp, pretty(blockArray, 2))


const firstPoSBlock = 15537394

echo("Creating JSON file with Proof of Work data")
let t0 = cpuTime()
writeBlocksToFile("../../static/pow.json", loadAllJSONBlocks("../../static/block_data", lessThan=firstPoSBlock))
let t1 = cpuTime()
echo(fmt"Execution time: {t1 - t0}")


echo("Creating JSON file with Proof of Stake data")
writeBlocksToFile("../../static/pos.json", loadAllJSONBlocks("../../static/block_data", greaterOrEqualThan=firstPoSBlock))
let t2 = cpuTime()

echo(fmt"Execution time: {t2 - t1}")
MinX = 240
MaxX = 292
MinY = -90
MaxY = -57

--[[
MinX = 20
MaxX = 30
MinY = -10
MaxY = -5
]]

function Simulate(dx, dy)
	local x = 0
	local y = 0
	local maxY = -99999

	while true do
		x = x + dx
		y = y + dy
		
		if y > maxY then
			maxY = y
		end

		if dx > 0 then
			dx = dx - 1
		end

		dy = dy - 1

		if dx == 0 and x < MinX then
			-- undershot and we'll never get there.
			return -1, maxY
		end

		if x > MaxX and y > MaxY then
			-- overshot
			return 1, maxY
		end

		if x >= MinX and x <= MaxX and y >= MinY and y <= MaxY then
			-- Within bounds.
			return 0, maxY
		end

		if y < MinY then
			if x < MaxX then
				-- undershot
				return -1, maxY
			elseif x > MinX then
				-- overshot
				return 1, maxY
			end
		end
	end
	return nil, 0
end

function FindDy(dx)
	local dy
	local allUnder = true
	local maxY = -9999

	for dy = 1,9999 do
		local res, yy = Simulate(dx, dy)

		if res == 0 then
			-- a hit.
			if yy > maxY then
				maxY = yy
				print("HRRRRR", maxY, dx, dy)
			end
			allUnder = false
		elseif res > 0 then
			allUnder = false
		end
	end

	if allUnder then
		return nil
	end

	return dy
end

function Part1()
	-- smallest dx that can get us there with the leftward drag, based on
	-- https://www.wolframalpha.com/input/?i=m%3D+%28sum+of+x+from+1+to+x%29%2C+solve+for+x
	local from = math.floor((math.sqrt(8 * MinX + 1) - 1) / 2)
	-- `to` is probably bogus but works accidentally.
	local to = math.ceil((math.sqrt(8 * MaxX + 1) - 1) / 2)

	for dx = from, to do
		local dy = FindDy(dx)
		if dy ~= nil then
			print(dx, dy)
		end
		print("  ", dx)
	end
end

function Part2()
	local hits = 0
	-- naive grid search.
	for dx = 1, MaxX do
		for dy = MinY, 9999 do
			local res, _ = Simulate(dx, dy)
			if res == 0 then
				hits = hits + 1
			elseif res > 0 then
				break
			end
		end
	end

	print(hits)
end

Part2()

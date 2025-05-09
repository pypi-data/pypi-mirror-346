from manim import *
import math
from typing import Optional, Tuple
import heapq

class ManimTool:
	def ChineseMathTex(*texts, color=WHITE, font="SimSun", font_size=DEFAULT_FONT_SIZE, tex_to_color_map={}):
		tex_template = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
		tex_template.add_to_preamble(r"\usepackage{amsmath}")
		tex_template.add_to_preamble(r"\usepackage{xeCJK}")
		tex_template.add_to_preamble(rf"\setCJKmainfont{{{font}}}")

		combined_chinesetext = []
		for text in texts:
			chinesetext = ""
			for i in range(len(text)):
				if ('\u4e00' <= text[i] <= '\u9fff') or ('\u3000' <= text[i] <= '\u303f') or ('\uff00' <= text[i] <= '\uffef'):
					chinesetext += rf"\text{{{text[i]}}}"
				else:
					chinesetext += text[i]
			combined_chinesetext.append(chinesetext)

		new_dict = {}
		for key in tex_to_color_map.keys():
			new_key = ""
			for char in key:
				if ('\u4e00' <= char <= '\u9fff') or ('\u3000' <= char <= '\u303f') or ('\uff00' <= char <= '\uffef'):
					new_key += rf"\text{{{char}}}"
				else:
					new_key += char
			new_dict[new_key] = tex_to_color_map[key]

		return MathTex(*combined_chinesetext, tex_template=tex_template, color=color, font_size=font_size, tex_to_color_map=new_dict)

	def YellowCircle(dot1, dot2):
		radius = np.linalg.norm(dot1.get_center() - dot2.get_center())
		circle = Circle(radius=radius).move_to(dot1.get_center()).set_color(YELLOW)
		return circle

	def YellowLine(start, end):
		line = Line(start=start, end=end).set_color(YELLOW)
		return line

	def MathTexLine(start, end, mathtex, color=WHITE, font_size=DEFAULT_FONT_SIZE, direction=UP, buff=0.5):
		line = Line(start=start, end=end).set_color(color)
		tex = ChineseMathTex(mathtex, color=color, font_size=font_size).next_to(line, direction, buff=buff)
		return VGroup(tex, line)

	def LabelDot(dot_label, dot_pos, label_pos=DOWN, buff=0.1):
		dot = Dot().move_to(dot_pos)
		label = MathTex(dot_label).next_to(dot, label_pos, buff=buff)
		return VGroup(label, dot)

	def MathTexBrace(start, end, mathtex, color=WHITE, font_size=DEFAULT_FONT_SIZE, direction=UP, buff=0.5):
		brace = Brace(Line(start=start, end=end), direction=direction).set_color(color)
		tex = ChineseMathTex(mathtex, color=color, font_size=font_size).next_to(brace, direction, buff=buff)
		return VGroup(tex, brace)

	def MathTexDoublearrow(start, end, mathtex, color=WHITE, font_size=DEFAULT_FONT_SIZE, direction=UP, buff=0.5):
		doublearrow = DoubleArrow(start=start, end=end)
		tex = ChineseMathTex(mathtex, color=color, font_size=font_size).next_to(doublearrow, direction, buff=buff)
		return VGroup(tex, doublearrow)

	def CircleInt(circle1, circle2):
		circle1_center = circle1.get_center()
		circle1_radius = circle1.radius
		circle2_center = circle2.get_center()
		circle2_radius = circle2.radius
		x1, y1, _ = circle1_center
		x2, y2, _ = circle2_center
		d = math.sqrt((x2 - x1) ** 2+(y2 - y1) ** 2)
		if d > circle1_radius + circle2_radius or d < abs(circle1_radius - circle2_radius):
			return None
		a = (circle1_radius ** 2 - circle2_radius ** 2 + d ** 2)/(2 * d)
		h = math.sqrt(circle1_radius ** 2 - a ** 2)
		xm = x1 + a * (x2 - x1)/d
		ym = y1 + a * (y2 - y1)/d
		xs1 = xm + h * (y2 - y1)/d
		xs2 = xm - h * (y2 - y1)/d
		ys1 = ym - h * (x2 - x1)/d
		ys2 = ym + h * (x2 - x1)/d
		return [xs1, ys1, 0], [xs2, ys2, 0]

	def LineCircleInt(line, circle):
		p1 = line.get_start()
		p2 = line.get_end()
		c = circle.get_center()
		r = circle.radius
		dx, dy, _ = p2 - p1
		cx, cy, _ = p1 - c
		a = dx**2 + dy**2
		b = 2 * (dx * cx + dy * cy)
		c = cx**2 + cy**2 - r**2
		discriminant = b**2 - 4 * a * c
		if discriminant < 0:
			return None
		t1 = (-b + math.sqrt(discriminant)) / (2 * a)
		t2 = (-b - math.sqrt(discriminant)) / (2 * a)
		intersections = []
		for t in [t1, t2]:
			if 0 <= t <= 1:
				intersection = p1 + t * (p2 - p1)
				intersections.append(intersection)
		return intersections

	def LineInt(line1: Line, line2: Line) -> Optional[Tuple[float, float]]:
		def det(a, b):
			return a[0] * b[1] - a[1] * b[0]
		p1 = line1.get_start()[:2]
		p2 = line1.get_end()[:2]
		p3 = line2.get_start()[:2]
		p4 = line2.get_end()[:2]
		xdiff = (p1[0] - p2[0], p3[0] - p4[0])
		ydiff = (p1[1] - p2[1], p3[1] - p4[1])
		div = det(xdiff, ydiff)
		if div == 0:
			return None
		d = (det(p1, p2), det(p3, p4))
		x = det(d, xdiff) / div
		y = det(d, ydiff) / div
		return [x, y, 0]

	def ExtendLine(line: Line, extend_distance: float) -> Line:
		start_point = line.get_start()
		end_point = line.get_end()
		direction_vector = end_point - start_point
		unit_direction_vector = direction_vector / np.linalg.norm(direction_vector)
		new_start_point = start_point - extend_distance * unit_direction_vector
		new_end_point = end_point + extend_distance * unit_direction_vector
		extended_line = YellowLine(start=new_start_point, end=new_end_point)
		return extended_line
	  
class SortTool:
	def bubsort(arr, reverse=False):
	    n = len(arr)
	    for i in range(n):
	        for j in range(0, n - i - 1):
	            if (not reverse and arr[j] > arr[j + 1]) or (reverse and arr[j] < arr[j + 1]):
	                arr[j], arr[j + 1] = arr[j + 1], arr[j]
	    return arr

	def inssort(arr, reverse=False):
	    for i in range(1, len(arr)):
	        key = arr[i]
	        j = i - 1
	        while (not reverse and j >= 0 and key < arr[j]) or (reverse and j >= 0 and key > arr[j]):
	            arr[j + 1] = arr[j]
	            j -= 1
	        arr[j + 1] = key
	    return arr

	def selsort(arr, reverse=False):
	    n = len(arr)
	    for i in range(n):
	        idx = i
	        for j in range(i + 1, n):
	            if (not reverse and arr[j] < arr[idx]) or (reverse and arr[j] > arr[idx]):
	                idx = j
	        arr[i], arr[idx] = arr[idx], arr[i]
	    return arr

	def quicksort(arr, reverse=False):
	    if len(arr) <= 1:
	        return arr
	    else:
	        pivot = arr[0]
	        left = []
	        right = []
	        for x in arr[1:]:
	            if (not reverse and x <= pivot) or (reverse and x >= pivot):
	                left.append(x)
	            else:
	                right.append(x)
	        return quisort(left, reverse) + [pivot] + quisort(right, reverse)

	def mergesort(arr, reverse=False):
	    if len(arr) <= 1:
	        return arr
	    else:
	        mid = len(arr) // 2
	        left = mersort(arr[:mid], reverse)
	        right = mersort(arr[mid:], reverse)

	        merged = []
	        i = j = 0
	        while i < len(left) and j < len(right):
	            if (not reverse and left[i] < right[j]) or (reverse and left[i] > right[j]):
	                merged.append(left[i])
	                i += 1
	            else:
	                merged.append(right[j])
	                j += 1
	        merged.extend(left[i:])
	        merged.extend(right[j:])
	        return merged

	def heapsort(arr, reverse=False):
	    if reverse:
	        arr = [-x for x in arr]
	        heapq.heapify(arr)
	        sorted_arr = []
	        while arr:
	            sorted_arr.append(-heapq.heappop(arr))
	    else:
	        heapq.heapify(arr)
	        sorted_arr = []
	        while arr:
	            sorted_arr.append(heapq.heappop(arr))
	    return sorted_arr

	def shellsort(arr, reverse=False):
	    n = len(arr)
	    gap = n // 2
	    while gap > 0:
	        for i in range(gap, n):
	            temp = arr[i]
	            j = i
	            while (not reverse and j >= gap and arr[j - gap] > temp) or (reverse and j >= gap and arr[j - gap] < temp):
	                arr[j] = arr[j - gap]
	                j -= gap
	            arr[j] = temp
	        gap //= 2
	    return arr

	def cousort(arr, reverse=False):
	    if not arr:
	        return arr
	    max_val = max(arr)
	    min_val = min(arr)
	    range_of_elements = max_val - min_val + 1
	    count_arr = [0 for _ in range(range_of_elements)]
	    output_arr = [0 for _ in range(len(arr))]

	    for i in range(len(arr)):
	        count_arr[arr[i] - min_val] += 1

	    for i in range(1, len(count_arr)):
	        count_arr[i] += count_arr[i - 1]

	    i = len(arr) - 1 if not reverse else 0
	    step = -1 if not reverse else 1
	    while (not reverse and i >= 0) or (reverse and i < len(arr)):
	        output_arr[count_arr[arr[i] - min_val] - 1] = arr[i]
	        count_arr[arr[i] - min_val] -= 1
	        i += step

	    return output_arr

	def bucsort(arr, reverse=False):
	    if not arr:
	        return arr
	    min_val = min(arr)
	    max_val = max(arr)
	    bucket_range = (max_val - min_val) / len(arr)
	    buckets = [[] for _ in range(len(arr) + 1)]

	    for num in arr:
	        index = int((num - min_val) // bucket_range)
	        buckets[index].append(num)

	    sorted_arr = []
	    for bucket in buckets:
	        bucket.sort(reverse=reverse)
	        sorted_arr.extend(bucket)

	    if reverse:
	        sorted_arr.reverse()

	    return sorted_arr

	def radsort(arr, reverse=False):
	    if not arr:
	        return arr
	    max_num = max(arr)
	    exp = 1
	    while max_num // exp > 0:
	        n = len(arr)
	        output = [0] * n
	        count = [0] * 10

	        for i in range(n):
	            index = arr[i] // exp
	            count[index % 10] += 1

	        for i in range(1, 10):
	            count[i] += count[i - 1]

	        i = n - 1 if not reverse else 0
	        step = -1 if not reverse else 1
	        while (not reverse and i >= 0) or (reverse and i < len(arr)):
	            index = arr[i] // exp
	            output[count[index % 10] - 1] = arr[i]
	            count[index % 10] -= 1
	            i += step

	        for i in range(n):
	            arr[i] = output[i]
	        exp *= 10
	    return arr
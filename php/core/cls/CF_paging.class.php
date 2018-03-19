<?php
// 만든이 : 그네

class Paging
{
// constants
    const ERR_PAGING_ROW                    = 10001;
    const ERR_PAGING_SCALE                  = 10002;
    const ERR_PAGING_PART_INFO_INVALID      = 10003;
    const ERR_PAGING_PART_NO_NOT_INTEGER    = 10004;
    const ERR_PAGING_PART_COUNT_NOT_INTEGER = 10005;

// only static
    private function __construct () {}

/**
  * @param array
  *     int total       : 전체 게시물수
  *     int page        : 현제 페이지번호
  *     int row         : 페이지당 게시물 수
  *     int scale       : 페이징 블럭 (페이지에 보여질 번호판 수)
  *     string link     : page=xxx 를 제외한 모든 링크
  *        예) aaa.php?a=$a&b=$b&c=$c&page=$page 이런 링크가 필요하다면
  *             link = "a=$a&b=$b&c=$c";
  *     array group     : 분할정보 (division 정보)
  *         int no => int count
  *     boolean center  : 번호판 현재페이지 중앙처리 여부
  * @param part         : boolean - 데이타를 group(division) 화 하는지의 여부
  * @return array
  *     total           : 전체 게시물 수
  *     page            : 현제 페이지 번호
  *     totalpage       : 총 페이지 수
  *     prev_link       : 이전 링크
  *     paging          : 번호판 리스트
  *     next_link       : 다음 링크
  *     start_link      : 처음 링크
  *     end_link        : 마지막 링크
  *     enable_prev     : 이전페이지 가능한가?
  *     enable_next     : 다음페이지 가능한가?
  *
  *     object query    : group 화 정보  (쿼리용 변수)
  *         int limit   : 쿼리에서 사용할 limit
  *         int offset  : 쿼리에서 사용할 offset
  *         array group : 쿼리에서 사용할 group number list
  */

    public static function draw (array $arr, $part = false)
    {
        $total = intval($arr['total']);
        $page = intval($arr['page']);
        $row = intval($arr['row']);
        $scale = intval($arr['scale']);
        $link = isset($arr['link']) ? $arr['link'] : '';
        $group = isset($arr['group']) ? $arr['group'] : '';

		$amp = ($link) ? '&' : '';

   

        if($row < 1)
            throw new Exception (self::ERR_PAGING_ROW);
        if($scale < 1)
            throw new Exception (self::ERR_PAGING_SCALE);

        if($page < 1) $page = 1;
        $totalpage = ceil($total / $row);
        if($page > $totalpage) $page = $totalpage;
        if($page < 1) $page = 1;

        if($total > 0) {
            if($arr['center'] === true) {
                $_center = intval($scale / 2);
                $_remain = $scale % 2 ? true : false;

                if($page <= $_center)
                    $start = 1;
                elseif((($totalpage - $page) < $_center) && $_remain)
                    $start = $totalpage - $scale + 1;
                elseif((($totalpage - $page + 1) < $_center) && !$_remain)
                    $start = $totalpage - $scale + 1;
                else $start = $page - $_center;

                $prev = $page - $scale;
                $next = $page + $scale;
            }
            else {
                $start = (intval($page / $scale) * $scale) + 1;
                if(!($page % $scale)) $start -= $scale;

                $prev = $start - $scale;
                $next = $start + $scale;
            }
            if($start < 1) $start = 1;
            $end = $start + $scale - 1;
            if($end > $totalpage) $end = $totalpage;

            if($prev < 1) $prev = 1;
            if($next > $totalpage) $next = $totalpage;
        }

        for($i = $start; $i <= $end; $i++)
            $paging_loop[] = array('page_num' => $i,
                                   'page_link' => "page=".$i.$amp.$link);

        $count = count($paging_loop);
        if($count > 0) $paging_loop[$count-1]['end'] = 1;


        $limit = $row;
        $offset = ($page - 1) * $row;

		$_grp = (object)[];
        if(!$part) {
            $_grp->limit = $limit;
            $_grp->offset = $offset;
        }
        else {
            if(!is_array($group))
                throw new Exception(self::ERR_PAGING_PART_INFO_INVALID);

            try {$_grp = self::_make_query_info($group, $limit, $offset); }
                catch (Exception $e) { throw $e; }
        }

        $arr = array('total' => $total,
                     'page' => $page,
                     'totalpage' => $totalpage,
                     'prev_link' => 'page='.$prev.$amp.$link,
                     'paging' => $paging_loop,
                     'next_link' => 'page='.$next.$amp.$link,
                     'start_link' => 'page=1'.$amp.$link,
                     'end_link' => 'page='.$totalpage.$amp.$link,
                     'enable_prev' => ($start > 1) ? true : false,
                     'enable_next' => ($end < $totalpage) ? true : false,
                     'query' => $_grp
            );

        return $arr;
    }

    private static function _make_query_info(array $grp, $limit, $offset)
    {
        $start = $offset;
        $end = $offset + $limit;

        $sum = 0;
        $found = false;
        $pos = array();
        $_offset = 0;

        foreach($grp as $part => $count) {
            if(!is_int($part) || $part < 1)
                throw new Exception(self::ERR_PAGING_PART_NO_NOT_INTEGER);
            if(!is_int($count))
                throw new Exception(self::ERR_PAGING_PART_COUNT_NOT_INTEGER);

            $sum += $count;

            if($sum > $start) $found = true;
            if($found) {
                $pos[] = $part;
                if(!$_offset) $_offset = $offset + $count - $sum;
            }
            if($sum >= $end) break;
        }

        if(!is_array($pos)) throw new Exception(self::ERR_PAGING_PART_INFO_INVALID);


        $group->group = $pos;
        $group->offset = $_offset;
        $group->limit = $limit;

        return $group;
    }

    public static function get_errmsg ($const)
    {
        switch($const) {
            case self::ERR_PAGING_ROW:
                return '페이지당 출력수를 셋팅해 주세요';
            case self::ERR_PAGING_SCALE:
                return '페이징 블럭을 셋팅해 주세요';
            case self::ERR_PAGING_PART_INFO_INVALID:
                return '분할정보가 없거나 잘못되었습니다.';
            case self::ERR_PAGING_PART_NO_NOT_INTEGER:
                return '분할번호가 숫자가 아니거나 없습니다.';
            case self::ERR_PAGING_PART_COUNT_NOT_INTEGER:
                return '해당분할그룹의 정보가 숫자가 아닙니다.';
            default: return '알수 없는 에러입니다.';
        }
    }
}


$page = 1;
// example
$arr = array('total' => 175,
             'page' => $page,
             'row' => 10,
             'scale' => 5,
             'center' => true    // 추가
        );

try {$paging = Paging::draw($arr); }
catch (Exception $e) {
    print 'LINE: '.$e->getLine().' '
                  .C::get_errmsg($e->getmessage());
    exit;
}

echo '<pre>';
print_r($paging);
//$tpl->assign($paging);

// vim600: ts=4 sw=4

?>